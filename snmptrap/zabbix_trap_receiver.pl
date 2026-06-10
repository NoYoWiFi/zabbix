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

sub generate_trap_content {
    my ($pdu_info, $varbinds, $ip_address) = @_;
    
    my $content = '';
    
    # print trap header
    $content .= sprintf "%s ZBXTRAP %s\n", strftime($DateTimeFormat, localtime), $ip_address;
    
    # print the PDU info
    $content .= "PDU INFO:\n";
    foreach my $key(keys(%$pdu_info))
    {
        my $value = $pdu_info->{$key};
        if ($value !~ /^[[:print:]]*$/)
        {
            my $OctetAsHex = unpack('H*', $value);    # convert octet string to hex
            $value = "0x$OctetAsHex";        # apply 0x prefix for consistency
        }
        $content .= sprintf "  %-30s %s\n", $key, $value;
    }
    
    # print the variable bindings:
    $content .= "VARBINDS:\n";
    foreach my $x (@$varbinds)
    {
        $content .= sprintf "  %-30s type=%-2d value=%s\n", $x->[0], $x->[2], $x->[1];
    }
    $content .= "\n";  # 添加空行分隔不同的trap
    
    return $content;
}

NetSNMP::TrapReceiver::register("all", \&zabbix_receiver) or
    die "failed to register Zabbix SNMP trap receiver\n";
print STDOUT "Loaded Zabbix SNMP trap receiver with IP-based file storage\n";
