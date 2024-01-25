-- ============================================================================
-- Copyright (c) 2004-2021 New H3C Tech. Co., Ltd.  All rights reserved.
-- Description: This MIB will maintain the products MIB OID and management
--              properties root node for H3C products
--
-- Reference:
-- Version: V1.26
-- History:
--   V1.00 2006-04-19 created by longyin
--   V1.01 2007/08/09 add hh3cSiemMib by gaolong
--   V1.02 2007/09/25 add hh3cSurveillanceMIB, hh3cVMMan, hh3cPUMan,
--                    and hh3cMSMan by longyin
--   V1.03 2007/10/25 add hh3cStorageRef under hh3c,
--                    and hh3cStorageMIB, hh3cStorageSnap, hh3cDisk,
--                        hh3cRaid, hh3cLogicVolume under hh3cStorageRef
--                    and hh3cUps under hh3cCommon by longyin
--   V1.04 2007/11/27 add hh3cEOCCommon and hh3cHPEOC by longyin
--   V1.05 2007/12/27 add hh3cAFC and hh3cMultCDR by longyin
--   V1.06 2008/02/27 add hh3cMACInformation, hh3cFireWall, hh3cDSP by longyin
--   V1.07 2008/04/29 add hh3cNetMan by songhao
--   V1.08 2008/06/02 add hh3cStack, hh3cPosa by songhao
--   V1.09 2008/07/29 add hh3cWebAuthentication by songhao
--   V1.10 2008/08/26 add hh3cCATVTransceiver by songhao
--   V1.11 2008/12/03 add hh3cLpbkdt by songhao
--   V1.12 2009/02/27 add hh3cMultiMedia, hh3cDns, hh3c3GModem
--                    and hh3cPortal by songhao
--   V1.13 2009/05/18 add hh3clldp, hh3cDHCPServer, hh3cPPPoEServer,
--                        hh3cL2Isolate, hh3cSnmpExt by duyanbing
--   V1.14 2009/11/04 add hh3cVsi, hh3cEvc, hh3cMinm, hh3cblg, hh3cRS485 by shuaixiaojuan
--   V1.15 2010/03/16 add hh3cARPRatelimit, hh3cLI by songhao
--         2010/09/15 add hpNetworking by songhao
--   V1.16 2011/01/31 add hh3cDar, hh3cPBR by songhao
--   V1.17 2011/04/22 add hh3cAAANasId by duyanbing
--   V1.18 2012/04/19 add hh3cTeTunnel, hh3cLB, hh3cDldp2, hh3cWIPS, hh3cFCoE,
--                        hh3cDot11Sa by duyanbing
--   V1.19 2013/01/08 add hh3cInfoCenter, hh3cTRNG2, hh3cDhcp4, hh3cDhcpSnoop2,
--                        hh3cRmonExt, hh3cIPsecMonitorV2, hh3cSanAgg, hh3cSpb,
--                        hh3cPortExtender, hh3cSlbg, hh3cFdmi, hh3cFirmwareUpgrade,
--                        hh3cIssuUpgrade by songhao
--   V1.20 2013/04/26 add hh3cEvb, hh3cFcoeMode, hh3cMDC, hh3cQinQv2, hh3cVmap
--                    modify name of 127, 129, 132 under hh3cCommon by songhao
--   V1.21 2013/09/22 remove hh3cFdmi under hh3cCommon
--                    add hh3cL2tp, hh3cMultilinkPPPV2, hh3cBpa by songhao
--   V1.22 2014/01/27 add hh3cLocAAASrv, hh3cMplsExt, hh3cMplsTe, hh3cLicense,
--                        hh3cLBv2, hh3cSession, hh3cARPSourceSuppression, hh3cVxlan
--                        under hh3cCommon by songhao
--   V1.23 2014/04/27 add hh3cRddc, hh3cIpRanDcn, hh3cContext
--                    modify name of 129 under hh3cCommon by songhao
--   V1.24 2014/09/18 add hh3cJointMibs, hh3cMulticastSnoop, hh3cPvst, hh3cSmlk,
--                        hh3c8021XExt2, hh3cObjp, hh3cNvgre by songhao
--   V1.25 2015/04/23 add 157 to 162 under hh3cCommon by songhao
--   V1.26 2016/04/02 add 163 to 165 under hh3cCommon
--                    add hh3cJointVendorId by songhao
-- ============================================================================
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        