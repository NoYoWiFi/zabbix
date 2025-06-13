die()     { echo >&2 $"FATAL: $@" ; exit 1 ; }
error()   { echo >&2 $"ERROR: $@" ; }
error_q() { echo >&2 $"       $@" ; }
warn()    { echo >&2 $"WARNING: $@" ; }
warn_q()  { echo >&2 $"         $@" ; }
info()    { echo >&2 $" * $@" ; }
info_q()  { echo >&2 $"   $@" ; }
debug()   { test "$option_debug" != "1" || echo >&2 $"DEBUG: $@";  }


set_var()
{
    eval "$1=\"$2\""
}


root_prereq()
{
    test -z "$PGSETUP_TEST" || return 0
    test "$(id -u)" -eq 0 || die "$0 requires root access for this action"
}


read_config_file()
{
    local key="" val=""

    test -r "$1" || die "can't read file '$1'"

    for i in $2; do
        eval "unset __pg_conf_$i"
    done

    # No easy (and secure) way to read configuration files from bash script,
    # sorry.
    while read key val; do
        [[ $key =~ ^[a-zA-Z_][a-zA-Z0-9_]*$ ]] || return 1

        case " $2 " in
        *" $key "*)
            ;;
        *)
            warn "config file '$1':  unknown key '$key'"
            continue
            ;;
        esac

        # Strip double quotes
        case "$val" in
        \"*\")
            val=${val##\"}
            val=${val%%\"}
            ;;
        esac

        # Make it reasonably safe.  Keep dolar-sign escaped.
        eval "__pg_conf_$key=\$val"

    done < <(grep -v -e "^$" -e "^#" < "$1")
}


parse_upgrade_setup()
{
    local action="$1"
    local expected_id="$2"
    local id temp_major temp_engine temp_data_default temp_description

    local upgrade_confdir="/etc/postgresql-setup/upgrade"

    debug "using 'upgrade' confdir $upgrade_confdir"
    test -d "$upgrade_confdir" || die "can't read confdir $upgrade_confdir"

    local my_vars="id comment data_default engine description major scls \
        redhat_sockets_hack pghost_override package"
    while read conffile
    do
        read_config_file "$conffile" "$my_vars"

        if test help = "$action"; then
            echo "$__pg_conf_id - $__pg_conf_description"
        elif test list = "$action"; then
            echo "$__pg_conf_id $__pg_conf_major"
        elif test config = "$action"; then
            test "$__pg_conf_id" = "$expected_id" || continue
            debug "reading config $conffile"
            for i in $my_vars; do
                set_var "upgradefrom_$i" "\$__pg_conf_$i"

                local cm="config file '$conffile'"
                # 'scls' and 'redhat_sockets_hack' are used to adjust
                # environment and could be bash-injected.
                case "$i" in
                scls)
                    test -z "$upgrade_from_scls" \
                        || [[ $upgrade_from_scls =~ ^[-a-zA-Z0-9_\ ]+$ ]] \
                        || die "$cm: bad '$i' value '$upgrade_from_scls'"
                    ;;
                redhat_sockets_hack)
                    case "$upgradefrom_redhat_sockets_hack" in
                    yes|no|'')
                        ;;
                    *)
                        die "$cm: bad '$i' value"
                        ;;
                    esac
                    ;;
                esac
            done
            return 0
        fi
    done < <(LC_ALL=C ls -1 "$upgrade_confdir"/*.conf || :)

    case "$action" in
        help|list)
            return 0
            ;;
    esac
    return 1
}
