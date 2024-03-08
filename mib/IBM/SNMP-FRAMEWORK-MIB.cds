    �"An identifier that uniquely identifies a
                    securityModel of the Security Subsystem within the
                    SNMP Management Architecture.

                    The values for securityModel are allocated as
                    follows:

                    - The zero value is reserved.
                    - Values between 1 and 255, inclusive, are reserved
                      for standards-track Security Models and are
                      managed by the Internet Assigned Numbers Authority
                      (IANA).
                    - Values greater than 255 are allocated to
                      enterprise-specific Security Models.  An
                      enterprise-specific securityModel value is defined
                      to be:

                      enterpriseID * 256 + security model within
                      enterprise

                      For example, the fourth Security Model defined by
                      the enterprise whose enterpriseID is 1 would be
                      260.

                    This scheme for allocation of securityModel
                    values allows for a maximum of 255 standards-
                    based Security Models, and for a maximum of
                    255 Security Models per enterprise.

                    It is believed that the assignment of new
                    securityModel values will be rare in practice
                    because the larger the number of simultaneously
                    utilized Security Models, the larger the
                    chance that interoperability will suffer.
                    Consequently, it is believed that such a range
                    will be sufficient.  In the unlikely event that
                    the standards committee finds this number to be
                    insufficient over time, an enterprise number
                    can be allocated to obtain an additional 255
                    possible values.

                    Note that the most significant bit must be zero;
                    hence, there are 23 bits allocated for various
                    organizations to design and define non-standard
                    securityModels.  This limits the ability to
                    define new proprietary implementations of Security
                    Models to the first 8,388,608 enterprises.

                    It is worthwhile to note that, in its encoded
                    form, the securityModel value will normally
                    require only a single byte since, in practice,
                    the leftmost bits will be zero for most messages
                    and sign extension is suppressed by the encoding
                    rules.

                    As of this writing, there are several values
                    of securityModel defined for use with SNMP or
                    reserved for use with supporting MIB objects.
                    They are as follows:

                        0  reserved for 'any'
                        1  reserved for SNMPv1
                        2  reserved for SNMPv2c
                        3  User-Based Security Model (USM)
                   "              "An identifier that uniquely identifies a Message
                    Processing Model of the Message Processing
                    Subsystem within a SNMP Management Architecture.
                    The values for messageProcessingModel are
                    allocated as follows:

                    - Values between 0 and 255, inclusive, are
                      reserved for standards-track Message Processing
                      Models and are managed by the Internet Assigned
                      Numbers Authority (IANA).

                    - Values greater than 255 are allocated to
                      enterprise-specific Message Processing Models.
                      An enterprise messageProcessingModel value is
                      defined to be:

                      enterpriseID * 256 +
                           messageProcessingModel within enterprise

                      For example, the fourth Message Processing Model
                      defined by the enterprise whose enterpriseID
                      is 1 would be 260.

                    This scheme for allocating messageProcessingModel
                    values allows for a maximum of 255 standards-
                    based Message Processing Models, and for a
                    maximum of 255 Message Processing Models per
                    enterprise.

                    It is believed that the assignment of new
                    messageProcessingModel values will be rare
                    in practice because the larger the number of
                    simultaneously utilized Message Processing Models,
                    the larger the chance that interoperability
                    will suffer. It is believed that such a range
                    will be sufficient.  In the unlikely event that
                    the standards committee finds this number to be
                    insufficient over time, an enterprise number
                    can be allocated to obtain an additional 256
                    possible values.

                    Note that the most significant bit must be zero;
                    hence, there are 23 bits allocated for various
                    organizations to design and define non-standard
                    messageProcessingModels.  This limits the ability
                    to define new proprietary implementations of
                    Message Processing Models to the first 8,388,608
                    enterprises.

                    It is worthwhile to note that, in its encoded
                    form, the messageProcessingModel value will
                    normally require only a single byte since, in
                    practice, the leftmost bits will be zero for
                    most messages and sign extension is suppressed
                    by the encoding rules.

                    As of this writing, there are several values of
                    messageProcessingModel defined for use with SNMP.
                    They are as follows:

                        0  reserved for SNMPv1
                        1  reserved for SNMPv2c
                        2  reserved for SNMPv2u and SNMPv2*
                        3  reserved for SNMPv3
                   "              �"A Level of Security at which SNMP messages can be
                    sent or with which operations are being processed;
                    in particular, one of:

                      noAuthNoPriv - without authentication and
                                     without privacy,
                      authNoPriv   - with authentication but
                                     without privacy,
                      authPriv     - with authentication and
                                     with privacy.

                    These three values are ordered such that
                    noAuthNoPriv is less than authNoPriv and
                    authNoPriv is less than authPriv.
                   "              �"An SNMP engine's administratively-unique identifier.
                    Objects of this type are for identification, not for
                    addressing, even though it is possible that an
                    address may have been used in the generation of
                    a specific value.

                    The value for this object may not be all zeros or
                    all 'ff'H or the empty (zero length) string.

                    The initial value for this object may be configured
                    via an operator console entry or via an algorithmic
                    function.  In the latter case, the following
                    example algorithm is recommended.

                    In cases where there are multiple engines on the
                    same system, the use of this algorithm is NOT
                    appropriate, as it would result in all of those
                    engines ending up with the same ID value.

                    1) The very first bit is used to indicate how the
                       rest of the data is composed.

                       0 - as defined by enterprise using former methods
                           that existed before SNMPv3. See item 2 below.

                       1 - as defined by this architecture, see item 3
                           below.
                       Note that this allows existing uses of the
                       engineID (also known as AgentID [RFC1910]) to
                       co-exist with any new uses.

                    2) The snmpEngineID has a length of 12 octets.

                       The first four octets are set to the binary
                       equivalent of the agent's SNMP management
                       private enterprise number as assigned by the
                       Internet Assigned Numbers Authority (IANA).
                       For example, if Acme Networks has been assigned
                       { enterprises 696 }, the first four octets would
                       be assigned '000002b8'H.

                       The remaining eight octets are determined via
                       one or more enterprise-specific methods. Such
                       methods must be designed so as to maximize the
                       possibility that the value of this object will
                       be unique in the agent's administrative domain.
                       For example, it may be the IP address of the SNMP
                       entity, or the MAC address of one of the
                       interfaces, with each address suitably padded
                       with random octets.  If multiple methods are
                       defined, then it is recommended that the first
                       octet indicate the method being used and the
                       remaining octets be a function of the method.

                    3) The length of the octet strings varies.

                       The first four octets are set to the binary
                       equivalent of the agent's SNMP management
                       private enterprise number as assigned by the
                       Internet Assigned Numbers Authority (IANA).
                       For example, if Acme Networks has been assigned
                       { enterprises 696 }, the first four octets would
                       be assigned '000002b8'H.

                       The very first bit is set to 1. For example, the
                       above value for Acme Networks now changes to be
                       '800002b8'H.

                       The fifth octet indicates how the rest (6th and
                       following octets) are formatted. The values for
                       the fifth octet are:

                         0     - reserved, unused.

                         1     - IPv4 address (4 octets)
                                 lowest non-special IP address

                         2     - IPv6 address (16 octets)
                                 lowest non-special IP address

                         3     - MAC address (6 octets)
                                 lowest IEEE MAC address, canonical
                                 order

                         4     - Text, administratively assigned
                                 Maximum remaining length 27

                         5     - Octets, administratively assigned
                                 Maximum remaining length 27

                         6-127 - reserved, unused

                       127-255 - as defined by the enterprise
                                 Maximum remaining length 27
                   "              
4"An octet string containing administrative
                    information, preferably in human-readable form.

                    To facilitate internationalization, this
                    information is represented using the ISO/IEC
                    IS 10646-1 character set, encoded as an octet
                    string using the UTF-8 transformation format
                    described in [RFC2279].

                    Since additional code points are added by
                    amendments to the 10646 standard from time
                    to time, implementations must be prepared to
                    encounter any code point from 0x00000000 to
                    0x7fffffff.  Byte sequences that do not
                    correspond to the valid UTF-8 encoding of a
                    code point or are outside this range are
                    prohibited.

                    The use of control codes should be avoided.

                    When it is necessary to represent a newline,
                    the control code sequence CR LF should be used.

                    The use of leading or trailing white space should
                    be avoided.

                    For code points not directly supported by user
                    interface hardware or software, an alternative
                    means of entry and display, such as hexadecimal,
                    may be provided.

                    For information encoded in 7-bit US-ASCII,
                    the UTF-8 encoding is identical to the
                    US-ASCII encoding.

                    UTF-8 may require multiple bytes to represent a
                    single character / code point; thus the length
                    of this object in octets may be different from
                    the number of characters encoded.  Similarly,
                    size constraints refer to the number of encoded
                    octets, not the number of characters represented
                    by an encoding.

                    Note that when this TC is used for an object that
                    is used or envisioned to be used as an index, then
                    a SIZE restriction MUST be specified so that the
                    number of sub-identifiers for any object instance
                    does not exceed the limit of 128, as defined by
                    [RFC1905].

                    Note that the size of an SnmpAdminString object is
                    measured in octets, not characters.
                   "                                         &"The SNMP Management Architecture MIB"�"WG-EMail:   snmpv3@tis.com
                     Subscribe:  majordomo@tis.com
                                 In message body:  subscribe snmpv3

                     Chair:      Russ Mundy
                                 TIS Labs at Network Associates
                     postal:     3060 Washington Rd
                                 Glenwood MD 21738
                                 USA
                     EMail:      mundy@tis.com
                     phone:      +1 301-854-6889

                     Co-editor   Dave Harrington
                                 Cabletron Systems, Inc.
                     postal:     Post Office Box 5005
                                 Mail Stop: Durham
                                 35 Industrial Way
                                 Rochester, NH 03867-5005
                                 USA
                     EMail:      dbh@ctron.com
                     phone:      +1 603-337-7357

                     Co-editor   Randy Presuhn
                                 BMC Software, Inc.
                     postal:     965 Stewart Drive
                                 Sunnyvale, CA 94086
                                 USA
                     EMail:      randy_presuhn@bmc.com
                     phone:      +1 408-616-3100

                     Co-editor:  Bert Wijnen
                                 IBM T.J. Watson Research
                     postal:     Schagen 33
                                 3461 GL Linschoten
                                 Netherlands
                     EMail:      wijnen@vnet.ibm.com
                     phone:      +31 348-432-794
                    " "9901190000Z" "9711200000Z" l"Updated editors' addresses, fixed typos.
                     Published as RFC2571.
                    " C"The initial version, published in RFC 2271.
                    "       -- 19 January 1999
           �"Registration point for standards-track
                     authentication protocols used in SNMP Management
                     Frameworks.
                    "               �"Registration point for standards-track privacy
                     protocols used in SNMP Management Frameworks.
                    "                       K"An SNMP engine's administratively-unique identifier.
                   "                       �"The number of times that the SNMP engine has
                    (re-)initialized itself since snmpEngineID
                    was last configured.
                   "                      �"The number of seconds since the value of
                    the snmpEngineBoots object last changed.
                    When incrementing this object's value would
                    cause it to exceed its maximum,
                    snmpEngineBoots is incremented as if a
                    re-initialization had occurred, and this
                    object's value consequently reverts to zero.
                   "                      _"The maximum length in octets of an SNMP message
                    which this SNMP engine can send or receive and
                    process, determined as the minimum of the maximum
                    message size values supported among all of the
                    transports available to and supported by the engine.
                   "                               �"The compliance statement for SNMP engines which
                    implement the SNMP Management Framework MIB.
                   "                   �"A collection of objects for identifying and
                    determining the configuration and current timeliness
                    values of an SNMP engine.
                   "                    