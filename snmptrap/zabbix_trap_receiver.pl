$DateTimeFormat = '%H:%M:%S %Y/%m/%d';

use Fcntl qw(O_WRONLY O_APPEND O_CREAT);
use POSIX qw(strftime);
use File::Path qw(make_path);

# IP trap文件存储基础目录
my $IP_TRAP_BASE = '/var/log/loki/snmptraps';

sub zabbix_receiver
{
    my (%pdu_info) = %{$_[0]};
    my (@varbinds) = @{$_[1]};
    
    # 获取主机IP地址
    my $hostname = $pdu_info{'receivedfrom'} || 'unknown';
    my $ip_address = 'unknown';
    if ($hostname ne 'unknown')
    {
        $hostname =~ /\[(.*?)\].*/;                    # format: "UDP: [127.0.0.1]:41070->[127.0.0.1]"
        $ip_address = $1 || 'unknown';
    }
    
    # 为IP地址创建安全的文件名（替换特殊字符）
    my $safe_ip = $ip_address;
    $safe_ip =~ s/[^a-zA-Z0-9._-]/_/g;
    
    # IP特定的trap文件路径
    my $ip_trap_file = "$IP_TRAP_BASE/${safe_ip}.log";
    
    # 创建目录（如果不存在）
    make_path($IP_TRAP_BASE) unless -d $IP_TRAP_BASE;
    
    # 处理trap内容到变量中，避免重复读取STDIN
    my $trap_content = generate_trap_content(\%pdu_info, \@varbinds, $ip_address);
    
    # 按IP地址存储到不同文件
    unless (sysopen(IP_FILE, $ip_trap_file, O_WRONLY|O_APPEND|O_CREAT, 0666))
    {
        print STDERR "Cannot open [$ip_trap_file]: $!\n";
        return NETSNMPTRAPD_HANDLER_FAIL;
    }
    print IP_FILE $trap_content;
    close(IP_FILE);
    
    return NETSNMPTRAPD_HANDLER_OK;
}

# 在 generate_trap_content 里改成 JSON 输出
use JSON;
$JSON::Blessed = 1;
$JSON::ConvertBlessed = 1;
sub generate_trap_content {
    my ($pdu_info, $varbinds, $ip_address) = @_;
    
    my %trap_data;
    
    # 基本信息
    $trap_data{timestamp} = strftime($DateTimeFormat, localtime);
    $trap_data{source} = "ZBXTRAP";
    $trap_data{ip_address} = $ip_address;
    $trap_data{format} = "snmptrap";
    
    # PDU info
    my %pdu;
    foreach my $key (keys(%$pdu_info)) {
        my $value = $pdu_info->{$key};
        if ($value !~ /^[[:print:]]*$/) {
            my $OctetAsHex = unpack('H*', $value);
            $value = "0x$OctetAsHex";
        }
        $pdu{$key} = $value;
    }
    $trap_data{pdu} = \%pdu;
    
    # VARBINDS
    my @vbs;
    foreach my $x (@$varbinds) {
        push @vbs, {
            oid => $x->[0],
            value => $x->[1],
            type => $x->[2]
        };
    }
    $trap_data{varbinds} = \@vbs;
    
    my $json = JSON->new->allow_blessed(1)->convert_blessed(1)->encode(\%trap_data);
    return $json . "\n";
}

NetSNMP::TrapReceiver::register("all", \&zabbix_receiver) or
    die "failed to register Zabbix SNMP trap receiver\n";
print STDOUT "Loaded Zabbix SNMP trap receiver with IP-based file storage\n";
