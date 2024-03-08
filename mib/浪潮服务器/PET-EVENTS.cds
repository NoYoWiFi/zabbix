1--/************************************************************************ 
--*                                                                       * 
--*  Copyright (c) 1998-2004 Intel Corporation. All Rights Reserved.      * 
--*                                                                       * 
--* Redistribution and use in source and binary forms, with or without    * 
--* modification, are permitted provided that the following conditions    * 
--* are met:                                                              * 
--*                                                                       * 
--*   a.. Redistributions of source code must retain the above copyright  * 
--*       notice, this list of conditions and the following disclaimer.   * 
--*   b.. Redistributions in binary form must reproduce the above         * 
--*       copyright notice, this list of conditions and the following     * 
--*       disclaimer in the documentation and/or other materials provided * 
--*       with the distribution.                                          * 
--*   c.. Neither the name of Intel Corporation nor the names of its      * 
--*       contributors may be used to endorse or promote products derived * 
--*       from this software without specific prior written permission.   * 
--*                                                                       * 
--* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS   * 
--* "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT     * 
--* LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR * 
--* A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT  * 
--* OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, * 
--* SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT      * 
--* LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, * 
--* DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON     * 
--* ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR    * 
--* TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF    * 
--* THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH  * 
--* DAMAGE.                                                               * 
--*                                                                       * 
--************************************************************************* 
--* Name                        : PetEvents.mib 
--* Description	                : MIB file for PET events 
--* Created                     : Wesdnesday, December 17, 2003 
--* Author                      : Intel Corporation 
--*  
--* $History:$  
--* 
--*             Date                    : March 7th,2002  
--*             Changed by              :  
--*             Change Description      : Updated MIB file  
--*							   
--*             Date                    : December 17th,2003  
--*             Changed by              :  
--*             Change Description      : Started with ASF MIB file 
--*                                        
--*************************************************************************/ 
--******************************************************************* 
--******************************************************************** 
--****                                                              ** 
--****    (C)Copyright 2011-2012, American Megatrends Inc.          ** 
--****                                                              ** 
--****    All Rights Reserved.                                      ** 
--****                                                              ** 
--****    5555 , Oakbrook Pkwy, Norcross,                           ** 
--****                                                              ** 
--****    Georgia - 30093, USA. Phone-(770)-246-8600.               ** 
--****                                                              ** 
--******************************************************************** 
--******************************************************************** 
--* Name                        : PETTrap.mib 
--* Description	                : Contains MIB for all standard sensor types 
--* Created                     : 8th August, 2011 
--* Author                      : AMI 
--*                                        
--*************************************************************************/ 
--********************************************************************************************
--Release Note:
--version  time		author   	note
--v1.0     20110808     AMI      	Contains MIB for all standard sensor types 
--v1.1     20140801     Inspur-wxl	add immtrapg and its children
--v1.2	   20141010     Inspur-wxl	fix insert hdd alert remove, remove hdd alert insert.
--v1.3     20141021	Inspur-wxl	add oem MemError and CPUERROR; modify enterprises id from 3183 to 37945
--v1.4	   20150310	Inspur-wxl	Remove "_", for linux cmd line error to load mib.
--v2.1	   20151104	Inspur-wxl	support v1/v2/v3.
--********************************************************************************************/ 
                 g"Slot / Connector - Not Ready for Device Installation. Typically, this means that the slot power is on"           �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Not Ready for Device Installation" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "ROM boot Incomplete"           m--#TYPE       "OS Boot Event" 
--#SUMMARY    "ROM boot Incomplete" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 "OEM System Boot Event Cleared"           |--#TYPE       "System Event" 
--#SUMMARY    "OEM System Boot Event Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 1"Memory event - Critical Overtemperature Cleared"           �--#TYPE       "Memory Event" 
--#SUMMARY    "Memory event - Critical Overtemperature Cleared"s 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ("OS Watchdog NMI / Diagnostic Interrupt"           �--#TYPE       "Watchdog Event" 
--#SUMMARY    "OS Watchdog NMI / Diagnostic Interrupt" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Reset Button pressed."           {--#TYPE       "Button/Switch Event" 
--#SUMMARY    "Reset Button pressed." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 0"Critical Interrupt, software NMI error Cleared"           �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, software NMI error Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Watchdog timer Reset"           o--#TYPE       "Watchdog Event" 
--#SUMMARY    "Watchdog timer reset" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 5"OS Stop / Shutdown - Soft Shutdown initiated by PEF"           �--#TYPE       "OS Stop / Shutdown Event" 
--#SUMMARY    "OS Stop / Shutdown - Soft Shutdown initiated by PEF" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 E"Critical Fan Over Speed problem (Upper critical, going low) Cleared"           �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Over Speed Warning (Upper critical, going low) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 C"Cooling Device Over Speed Warning (Upper non-critical, going low)"           �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Over Speed Warning (Upper non-critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 "Watchdog Reset Deasserted"           u--#TYPE       "Watchdog Event" 
--#SUMMARY    "Watchdog Reset Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 6"System Boot / Restart - Automatic boot to diagnostic"           �--#TYPE       "System Boot / Restart Event" 
--#SUMMARY    "System Boot / Restart - Automatic boot to diagnostic" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 2"Hard Disk Drive Rebuild/Remap Aborted Deasserted"           �--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive Rebuild/Remap Aborted Deasserted(completed)" 
--#ARGUMENTS    {} 
--#SEVERITY     INFORMATIONAL 
 H"Entity contains an invalid or unsupported firmware or software version"           �--#TYPE       "Version Change Event" 
--#SUMMARY    "Entity contains an invalid or unsupported firmware or software version" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 &"Monitor ASIC / IC Failure Deasserted"           �--#TYPE       "Monitor ASIC / IC Event" 
--#SUMMARY    "Monitor ASIC / IC Failure Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 �"OS Stop / Shutdown - Stop during OS load / initialization. Unexpected error uring system startup. Stopped waiting for input or power cycle/reset"           �--#TYPE       "OS Stop / Shutdown Event" 
--#SUMMARY    "OS Stop / Shutdown - Stop during OS load / initialization" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 P"Critical Under-Temperature problem (Lower non-recoverable, going high) Cleared"           �--#TYPE       "Temperature Event" 
--#SUMMARY    "Under-Temperature Warning (Lower non-recoverable, going high) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 4"Cable / Interconnect Predictive Failure Deasserted"           �--#TYPE       "Other Cable / Interconnect Event" 
--#SUMMARY    "Cable / Interconnect Predictive Failure Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "I/O Card Area Intrusion"           |--#TYPE       "Chassis Intrusion Event" 
--#SUMMARY    "I/O Card Area Intrusion" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 ""CPU0 Channel3 Dimm0 memory Error"             K"OS Stop / Shutdown - Graceful Shutdown (system graceful power down by OS)"           �--#TYPE       "OS Stop / Shutdown Event" 
--#SUMMARY    "OS Stop / Shutdown - Graceful Shutdown" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Spare Unit of Memory detected"           |--#TYPE       "Memory Event" 
--#SUMMARY    "Spare Unit of Memory detected" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ?"Chassis Intrusion (Physical Security Violation) Event Cleared"           �--#TYPE       "Chassis Intrusion Event" 
--#SUMMARY    "Chassis Intrusion( Physical Security Violation) Event Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ?"Under-Voltage Warning (Lower non-critical, going low) Cleared"           �--#TYPE       "Voltage Event" 
--#SUMMARY    "Under-Voltage Warning (Lower non-critical, going low) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 3"Critical Interrupt, PCI SERR parity error Cleared"           �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, PCI SERR parity error Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "System Firmware Hang"           �--#TYPE       "System Firmware Progress Event" 
--#SUMMARY    "System Firmware Hang" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 )"Memory event - Critical Overtemperature"           �--#TYPE       "Memory Event" 
--#SUMMARY    "Memory event - Critical Overtemperature" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 /"Processor Throttled (Processor Speed Reduced)"           �--#TYPE       "Processor Event" 
--#SUMMARY    "Processor Throttled (Processor Speed Reduced)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 W"Critical Cooling Device Under Speed problem (Lower non-recoverable, going low)Cleared"           �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Under Speed Warning (Lower non-recoverable, going low)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 G"Critical Over-Temperature problem (Upper critical, going high)Cleared"           �--#TYPE       "Temperature Event" 
--#SUMMARY    "Over-Temperature Warning (Upper critical, going high)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ""Processor Area Intrusion Cleared"           �--#TYPE       "Chassis Intrusion Event" 
--#SUMMARY    "Processor Area Intrusion Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 1"Chassis Intrusion - Drive Bay Violation Cleared"           �--#TYPE       "Chassis Intrusion Event" 
--#SUMMARY    "Chassis Intrusion - Drive Bay Violation Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ("Terminator Predictive Failure Asserted"           �--#TYPE       "Terminator Event" 
--#SUMMARY    "Terminator Predictive Failure Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 +"Add-in Card Predictive Failure Deasserted"           �--#TYPE       "Add-in Card Event" 
--#SUMMARY    "Add-in Card Predictive Failure Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "C: boot incomplete"           l--#TYPE       "OS Boot Event" 
--#SUMMARY    "C: boot incomplete" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 O"Critical Cooling Device Over Speed problem (Upper non-recoverable, going low)"           �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Over Speed Warning (Upper non-recoverable, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 /"OS Stop / Shutdown - Agent Started Responding"           �--#TYPE       "OS Stop / Shutdown Event" 
--#SUMMARY    "OS Stop / Shutdown - Agent Started Responding" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "A: boot incomplete"           l--#TYPE       "OS Boot Event" 
--#SUMMARY    "A: boot incomplete" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 '"Hard Disk Drive Rebuild/Remap Aborted"           �--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive Rebuild/Remap Aborted" 
--#ARGUMENTS    {} 
--#SEVERITY     INFORMATIONAL 
 ,"Microcontroller/Coprocessor State Asserted"           �--#TYPE       "Microcontroller/Coprocessor Event" 
--#SUMMARY    "Microcontroller/Coprocessor State Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ;"Over-Temperature Warning (Upper non-critical, going high)"           �--#TYPE       "Temperature Event" 
--#SUMMARY    "Over-Temperature Warning (Upper non-critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 &"Memory Configuration Error detected."           �--#TYPE       "Memory Event" 
--#SUMMARY    "Memory Configuration Error  detected." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 A"Hard Disk Drive Rebuild/Remap in progress Deasserted(completed)"           �--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive Rebuild/Remap in progress Deasserted(completed)" 
--#ARGUMENTS    {} 
--#SEVERITY     INFORMATIONAL 
 $"Power unit AC/Power input restored"           �--#TYPE       "Power unit event" 
--#SUMMARY    "Power unit AC/Power input restored" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
  "Management controller off-line"           �--#TYPE       "Management Subsystem Health Event" 
--#SUMMARY    "Management controller off-line" 
--#ARGUMENTS  {} 
--#SEVERITY   MAJOR 
 �"OS Stop / Shutdown - Graceful Stop (system powered up, but normal OS operation has shut down and system is awaiting reset pushbutton, powercycle or other external input)"           �--#TYPE       "OS Stop / Shutdown Event" 
--#SUMMARY    "OS Stop / Shutdown - Graceful Stop" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 @"Critical Under-Temperature problem (Lower critical, going low)"           �--#TYPE       "Temperature Event" 
--#SUMMARY    "Under-Temperature Warning (Lower critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 9"Entity is of an invalid or unsupported hardware version"           �--#TYPE       "Version Change Event" 
--#SUMMARY    "Entity is of an invalid or unsupported hardware version" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 '"Power Unit Predictive Failure Cleared"           �--#TYPE       "Power unit event" 
--#SUMMARY    "Power Unit Predictive Failure Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Thermal Trip Occured"           o--#TYPE       "Chip Set Event" 
--#SUMMARY    "Thermal Trip Occured" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 &"Slot / Connector - Slot Power is Off"           �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Slot Power is Off" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Chip Set State Asserted"           x--#TYPE       "Chip Set Event" 
--#SUMMARY    "Chip Set State Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "A HDD Fault LED is ON."           {--#TYPE       "Drive Slot Event" 
--#SUMMARY    "Hard Disk Drive Fault LED is ON." 
--#ARGUMENTS  {} 
--#SEVERITY   MAJOR 
 +"Critical Interrupt, PCI SERR parity error"           �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, PCI SERR parity error" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 *"Setup Password Violation Attempt Cleared"           �--#TYPE       "Platform Securtiy Violation Attempt Event" 
--#SUMMARY    "Setup Password Violation Attempt Cleared"  
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 >"Over-Current Warning (Upper non-critical, going low) Cleared"           �--#TYPE       "Current Event" 
--#SUMMARY    "Over-Current Warning (Upper non-critical, going low) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ,"Module/Board Predictive Failure Deasserted"           �--#TYPE       "Module/Board Event" 
--#SUMMARY    "Module/Board Predictive Failure Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ."Undetermined system hardware failure Cleared"           �--#TYPE       "System Event" 
--#SUMMARY    "Undetermined system hardware failure Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 ,"OS Watchdog pre-timeout Interrupt, non-NMI"           �--#TYPE       "Watchdog Event" 
--#SUMMARY    "OS Watchdog pre-timeout Interrupt, non-NMI" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 :"Fan Under Speed Warning (Lower non-critical, going high)"           �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Under Speed Warning (Lower non-critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 %"Generic Discrete Voltage  (Monitor)"           �--#TYPE	      "Voltage Event" 
--#SUMMARY    "Generic Discrete Voltage (Monitor)" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Chassis State Asserted"           v--#TYPE       "Chassis Event" 
--#SUMMARY    "Chassis State Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 :"Critical Interrupt, EISA Fail Safe Timeout Event Cleared"           �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, EISA Fail Safe Timeout Event Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Power unit 240VA Power Down"           ~--#TYPE       "Power unit event" 
--#SUMMARY    "Power unit 240VA Power Down" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Chip Set State Deasserted"           z--#TYPE       "Chip Set Event" 
--#SUMMARY    "Chip Set State Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 9"Fan Over Speed Warning (Upper non-critical, going high)"           �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Over Speed Warning (Upper non-critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 @"Fan Over Speed Warning (Upper non-critical, going high)Cleared"           �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Over Speed Warning (Upper non-critical, going high)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 V"Critical Cooling Device Over Speed problem (Upper non-recoverable, going low)Cleared"           �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Over Speed Warning (Upper non-recoverable, going low)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Power Unit Predictive Failure"           �--#TYPE       "Power unit event" 
--#SUMMARY    "Power Unit Predictive Failure" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "SEL Area Reset/Cleared"           y--#TYPE       "System Event Log" 
--#SUMMARY    "SEL Area Reset/Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Found bootable media"           w--#TYPE       "Boot Error Event" 
--#SUMMARY    "Found bootable media" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 1"System Boot / Restart - User requested PXE boot"           �--#TYPE       "System Boot / Restart Event" 
--#SUMMARY    "System Boot / Restart - User requested PXE boot" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 M"Critical Fan Over Speed problem (Upper non-recoverable, going high) Cleared"           �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Under Speed Warning (Upper non-recoverable, going high) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Processor Configuration Error"           z--#TYPE       "Processor Event" 
--#SUMMARY    "Processor Configuration Error" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 $"Hard Disk Drive Predictive Failure"           �--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive Predictive Failure" 
--#ARGUMENTS    {} 
--#SEVERITY     INFORMATIONAL 
 H"Critical Cooling Device Over Speed problem (Upper critical, going low)"           �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Over Speed Warning (Upper critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 *"Generic Critical Voltage Problem Cleared"           �--#TYPE       "Voltage Event" 
--#SUMMARY    "Generic Critical Voltage Problem Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 !"User Password Violation Attempt"           �--#TYPE       "Platform Securtiy Violation Attempt Event" 
--#SUMMARY    "User Password Violation Attempt" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "Unauthorized dock"           v--#TYPE       "Chassis Intrusion Event" 
--#SUMMARY    "Unauthorized dock" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 R"Critical Cooling Device Under Speed problem (Lower critical, going high) Cleared"           �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Under Speed Warning (Lower critical, going high) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 C"The Entity identified by the Entity ID for the sensor is present."           v--#TYPE       "Entity Presence Event" 
--#SUMMARY    "Entity Present" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 @"Uncorrectable ECC or other uncorrectable memory error Cleared."           �--#TYPE       "Memory Event" 
--#SUMMARY    "Uncorrectable ECC or other uncorrectable memory error Cleared." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "FRU Inactive"           n--#TYPE       "FRU State Event" 
--#SUMMARY    "FRU Inactive" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ;"Microcontroller/Coprocessor Predictive Failure Deasserted"           �--#TYPE       "Microcontroller/Coprocessor Event" 
--#SUMMARY    "Microcontroller/Coprocessor Predictive Failure Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 H"Critical Under-Temperature problem (Lower non-recoverable, going high)"           �--#TYPE       "Temperature Event" 
--#SUMMARY    "Under-Temperature Warning (Lower non-recoverable, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 L"Software or F/W Change detected with associated Entity was not successful."           �--#TYPE       "Version Change Event" 
--#SUMMARY    "Software or F/W Change detected with associated Entity was not successful." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 <"Critical Under-Current problem (Lower critical, going low)"           �--#TYPE       "Current Event" 
--#SUMMARY    "Under-Current Warning (Lower critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 <"Generic Critical Voltage Problem Cleared(Transition to OK)"           �--#TYPE	      "Voltage Event" 
--#SUMMARY    "Generic Critical Voltage Problem Cleared(Transition to OK)" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Watchdog Timer interrupt"           y--#TYPE       "Watchdog Event" 
--#SUMMARY    "Watchdog Timer interrupt" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ;"Critical Over-Current problem (Upper critical, going low)"           �--#TYPE       "Current Event" 
--#SUMMARY    "Over-Current Warning (Upper critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 #"System Reconfigured Event Cleared"           �--#TYPE       "System Event" 
--#SUMMARY    "System Reconfigured Event Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 W"System Boot / Restart - Restart cause per Get System Restart Cause command Deasserted"           �--#TYPE       "System Boot / Restart Event" 
--#SUMMARY    "System Boot / Restart - Restart cause per Get System Restart Cause command Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 �"Run-time power fault has occurred. This state indicates 
  that one or more DC-DC converter have failed or are not operating 
  within nominal specifications."           �--#TYPE         "Power Unit Event" 
--#SUMMARY      "Run-time power fault has occurred." 
--#ARGUMENTS    {} 
--#SEVERITY     CRITICAL 
 "System Reconfigured"           r--#TYPE       "System Event" 
--#SUMMARY    "System Reconfigured" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 K"Critical Over-Voltage problem (Upper non-recoverable, going high) Cleared"           �--#TYPE       "Voltage Event" 
--#SUMMARY    "Under-Voltage Warning (Upper non-recoverable, going high) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 -"Boot Incomplete - boot device not specified"           �--#TYPE       "OS Boot Event" 
--#SUMMARY    "Boot Incomplete - boot device not specified" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 ""CPU0 Channel2 Dimm2 memory Error"             ""CPU0 Channel2 Dimm1 memory Error"             ""CPU0 Channel2 Dimm0 memory Error"             $"OS Watchdog Power Cycle Deasserted"           �--#TYPE       "Watchdog Event" 
--#SUMMARY    "OS Watchdog Power Cycle Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ,"Hard Disk Drive In Failed Array Deasserted"           �--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive In Failed Array Deasserted" 
--#ARGUMENTS    {} 
--#SEVERITY     CRITICAL 
 ]"OS Stop / Shutdown - System powered by reset pushbutton, powercycle or other external input"           �--#TYPE       "OS Stop / Shutdown Event" 
--#SUMMARY    "OS Stop / Shutdown - Graceful Shutdown Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "FRU Active"           l--#TYPE       "FRU State Event" 
--#SUMMARY    "FRU Active" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 %"Memory Configuration Error Cleared."           �--#TYPE       "Memory Event" 
--#SUMMARY    "Memory Configuration Error  Cleared." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 9"Microcontroller/Coprocessor Predictive Failure Asserted"           �--#TYPE       "Microcontroller/Coprocessor Event" 
--#SUMMARY    "Microcontroller/Coprocessor Predictive Failure Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 L"Critical Under-Voltage problem (Lower non-recoverable, going high) Cleared"           �--#TYPE       "Voltage Event" 
--#SUMMARY    "Under-Voltage Warning (Lower non-recoverable, going high) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ("Critical Interrupt, software NMI error"           �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, software NMI error" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 <"Critical Under-Voltage problem (Lower critical, going low)"           �--#TYPE       "Voltage Event" 
--#SUMMARY    "Under-Voltage Warning (Lower critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 %"Watchdog Timer interrupt Deasserted"           �--#TYPE       "Watchdog Event" 
--#SUMMARY    "Watchdog Timer interrupt Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Sleep Button pressed."           {--#TYPE       "Button/Switch Event" 
--#SUMMARY    "Sleep Button pressed." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ;"Critical Over-Voltage problem (Upper critical, going low)"           �--#TYPE       "Voltage Event" 
--#SUMMARY    "Over-Voltage Warning (Upper critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 I"Critical Under-Temperature problem (Lower critical, going high) Cleared"           �--#TYPE       "Temperature Event" 
--#SUMMARY    "Under-Temperature Warning (Lower critical, going high) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 G"Critical Over-Temperature problem (Upper non-recoverable, going high)"           �--#TYPE       "Temperature Event" 
--#SUMMARY    "Under-Temperature Warning (Upper non-recoverable, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 F"Generic Temperature Warning (Transition to Warning from less severe)"           �--#TYPE	      "Temperature Event" 
--#SUMMARY    "Generic Temperature Warning (Transition to Warning from less severe)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 P"System Boot / Restart - OS / run-time software initiated hard reset Deasserted"           �--#TYPE       "System Boot / Restart Event" 
--#SUMMARY    "System Boot / Restart - OS / run-time software initiated hard reset Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 /"System ACPI Power State - G3 - Mechanical Off"           �--#TYPE       "System ACPI Power State Event" 
--#SUMMARY    "System ACPI Power State - G3" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 X"System ACPI Power State - S4 / S5 soft-off, particular S4 / S5 state cannot be determi"           �--#TYPE       "System ACPI Power State Event" 
--#SUMMARY    "System ACPI Power State - S4 / S5 soft-off" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ?"Watchdog timer expired, status only (no action, no interrupt)"           q--#TYPE       "Watchdog Event" 
--#SUMMARY    "Watchdog timer expired" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 L"System ACPI Power State - G1 - sleeping (S1-S4 state cannot be determined)"           �--#TYPE       "System ACPI Power State Event" 
--#SUMMARY    "System ACPI Power State - G1" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Unauthorized dock Cleared"           �--#TYPE       "Chassis Intrusion Event" 
--#SUMMARY    "Unauthorized dock Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 K"Cooling Device Over Speed Warning (Upper non-critical, going low) Cleared"           �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Over Speed Warning (Upper non-critical, going low) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 +"Hard Disk Drive Rebuild/Remap in progress"           �--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive Rebuild/Remap in progress" 
--#ARGUMENTS    {} 
--#SEVERITY     INFORMATIONAL 
 E"Critical Fan Under Speed problem (Lower critical, going low)Cleared"           �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Under Speed Warning (Lower critical, going low)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 N"Critical Under-Temperature problem (Lower non-recoverable, going low)Cleared"           �--#TYPE       "Temperature Event" 
--#SUMMARY    "Under-Temperature Warning (Lower non-recoverable, going low)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Fan Area Intrusion"           w--#TYPE       "Chassis Intrusion Event" 
--#SUMMARY    "Fan Area Intrusion" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 A"Critical Under-Temperature problem (Lower critical, going high)"           �--#TYPE       "Temperature Event" 
--#SUMMARY    "Under-Temperature Warning (Lower critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 @"Fan Over Speed Warning (Upper non-critical, going low) Cleared"           �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Over Speed Warning (Upper non-critical, going low) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 &"Chip Set Predictive Failure Asserted"           �--#TYPE       "Chip Set Event" 
--#SUMMARY    "Chip Set Predictive Failure Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 >"Critical Fan Under Speed problem (Lower critical, going low)"           �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Under Speed Warning (Lower critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 G"Critical Under-Temperature problem (Lower critical, going low)Cleared"           �--#TYPE       "Temperature Event" 
--#SUMMARY    "Under-Temperature Warning (Lower critical, going low)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 6"Over-Voltage Warning (Upper non-critical, going low)"           �--#TYPE       "Voltage Event" 
--#SUMMARY    "Over-Voltage Warning (Upper non-critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 "Terminator State Deasserted"           ~--#TYPE       "Terminator Event" 
--#SUMMARY    "Terminator State Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 I"Critical Cooling Device Under Speed problem (Lower critical, going low)"           �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Under Speed Warning (Lower critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "User selected boot source"           |--#TYPE       "Boot Error Event" 
--#SUMMARY    "User selected boot source" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 '"Processor Configuration Error Cleared"           �--#TYPE       "Processor Event" 
--#SUMMARY    "Processor Configuration Error Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 0"OS Watchdog NMI / Diagnostic Interrupt Cleared"           �--#TYPE       "Watchdog Event" 
--#SUMMARY    "OS Watchdog NMI / Diagnostic Interrupt Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 2"Cooling Device Redundancy is in a degraded state"           �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Redundancy is in a degraded state" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 "SEL Almost Full Event Cleared"           �--#TYPE       "System Event Log" 
--#SUMMARY    "SEL Almost Full Event Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ="Critical Fan Over Speed problem (Upper critical, going low)"           �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Over Speed Warning (Upper critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "Processor Area Intrusion"           }--#TYPE       "Chassis Intrusion Event" 
--#SUMMARY    "Processor Area Intrusion" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 ?"Critical Fan Under Speed problem (Lower critical, going high)"           �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Under Speed Warning (Lower critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 J"Critical Cooling Device Under Speed problem (Lower critical, going high)"           �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Under Speed Warning (Lower critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "FRU Communication Lost"           x--#TYPE       "FRU State Event" 
--#SUMMARY    "FRU Communication Lost" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Sleep Button Released."           |--#TYPE       "Button/Switch Event" 
--#SUMMARY    "Sleep Button Released." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 )"A device is absent or has been removed."           �--#TYPE       "Entity Presence Event" 
--#SUMMARY    "A device is absent or has been removed." 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 ,"Hard Disk Drive Predictive Failure Cleared"           �--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive Predictive Failure Cleared" 
--#ARGUMENTS    {} 
--#SEVERITY     INFORMATIONAL 
 #"Boot Error - PXE Server not found"           --#TYPE       "Boot Error Event" 
--#SUMMARY    "Boot Error - PXE Server not found" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 +"Critical Interrupt, Bus Correctable Error"           �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, Bus Correctable Error" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 G"Critical Over-Temperature problem (Upper critical, going low) Cleared"           �--#TYPE       "Temperature Event" 
--#SUMMARY    "Over-Temperature Warning (Upper critical, going low) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 8" Hard Disk Drive Hot Spare (Ready to remove) Asserted "           �--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive Hot spare (Ready to Remove) " 
--#ARGUMENTS    {} 
--#SEVERITY     INFORMATIONAL 
 H"Correctable ECC / other correctable memory error logging limit reached"           �--#TYPE       "Memory Event" 
--#SUMMARY    "Correctable ECC / other correctable memory error logging limit reached" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Module/Board State Asserted"           �--#TYPE       "Module/Board Event" 
--#SUMMARY    "Module/Board State Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Module/Board State Deasserted"           �--#TYPE       "Module/Board Event" 
--#SUMMARY    "Module/Board State Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ;"Platform Alert - platform generated SNMP trap, OEM format"           �--#TYPE       "Platform Alert Event" 
--#SUMMARY    "Platform Alert- platform generated SNMP trap, OEM format" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 <"System Boot / Restart - User requested PXE boot Deasserted"           �--#TYPE       "System Boot / Restart Event" 
--#SUMMARY    "System Boot / Restart - User requested PXE boot Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "PEF Action Event Deasserted"           z--#TYPE       "System Event" 
--#SUMMARY    "PEF Action Event Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 '"Chassis Predictive Failure Deasserted"           �--#TYPE       "Chassis Event" 
--#SUMMARY    "Chassis Predictive Failure Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 >"Over-Voltage Warning (Upper non-critical, going low) Cleared"           �--#TYPE       "Voltage Event" 
--#SUMMARY    "Over-Voltage Warning (Upper non-critical, going low) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ("Spare Unit of Memory detected Deassert"           �--#TYPE       "Memory Event" 
--#SUMMARY    "Spare Unit of Memory detected Deassert" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ("Chip Set Predictive Failure Deasserted"           �--#TYPE       "Chip Set Event" 
--#SUMMARY    "Chip Set Predictive Failure Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 E"Critical Fan Over Speed problem (Upper critical, going high)Cleared"           �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Over Speed Warning (Upper critical, going high)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 C"Critical Under-Voltage problem (Lower critical, going low)Cleared"           �--#TYPE       "Voltage Event" 
--#SUMMARY    "Under-Voltage Warning (Lower critical, going low)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Event Type Logging Disabled"           --#TYPE       "System Event Log" 
--#SUMMARY    "Event Type Logging Disabled." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ]"OS Stop / Shutdown - System powered by reset pushbutton, powercycle or other external input"           �--#TYPE       "OS Stop / Shutdown Event" 
--#SUMMARY    "OS Stop / Shutdown - Soft Shutdown Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 K"Critical Fan Over Speed problem (Upper non-recoverable, going low)Cleared"           �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Over Speed Warning (Upper non-recoverable, going low)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 I"Critical Over-Voltage problem (Upper non-recoverable, going low)Cleared"           �--#TYPE       "Voltage Event" 
--#SUMMARY    "Over-Voltage Warning (Upper non-recoverable, going low)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 8"Fan Over Speed Warning (Upper non-critical, going low)"           �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Over Speed Warning (Upper non-critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 "Fan Area Intrusion Cleared"           �--#TYPE       "Chassis Intrusion Event" 
--#SUMMARY    "Fan Area Intrusion Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 G"Generic Voltage Warning (Transition to Non-Critical from less severe)"           �--#TYPE	      "Voltage Event" 
--#SUMMARY    "Generic Voltage Warning (Transition to Non-Critical from less severe)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 <"Critical Over-Current problem (Upper critical, going high)"           �--#TYPE       "Current Event" 
--#SUMMARY    "Over-Current Warning (Upper critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 H"Software or F/W Change detected with associated Entity was successful."           �--#TYPE       "Version Change Event" 
--#SUMMARY    "Software or F/W Change detected with associated Entity was successful." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 J"Critical Under-Voltage problem (Lower non-recoverable, going low)Cleared"           �--#TYPE       "Voltage Event" 
--#SUMMARY    "Under-Voltage Warning (Lower non-recoverable, going low)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ""CPU0 Channel1 Dimm2 memory Error"             ""CPU0 Channel1 Dimm1 memory Error"             "Processor Disabled"           t--#TYPE       "Processor Event" 
--#SUMMARY    "Processor Disabled" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ""CPU0 Channel1 Dimm0 memory Error"             ="Correctable ECC or other correctable memory error detected."           �--#TYPE       "Memory Event" 
--#SUMMARY    "Correctable ECC or other correctable memory error detected." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 K"Critical Over-Current problem (Upper non-recoverable, going high) Cleared"           �--#TYPE       "Current Event" 
--#SUMMARY    "Under-Current Warning (Upper non-recoverable, going high) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 D"Cooling Device Over Speed Warning (Upper non-critical, going high)"           �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Over Speed Warning (Upper non-critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 "System Firmware Hang Cleared"           �--#TYPE       "System Firmware Progress Event" 
--#SUMMARY    "System Firmware Hang Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 d"Slot / Connector - Ready for Device Installation. Typically, this means that the slot power is off"           �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Ready for Device Installation" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 '"POST Memory Resize Failure Deasserted"           �--#TYPE       "POST Memory Resize Event" 
--#SUMMARY    "POST Memory Resize Failure Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 -"OS Stop / Shutdown - Run-time Critical Stop"           �--#TYPE       "OS Stop / Shutdown Event" 
--#SUMMARY    "OS Stop / Shutdown - Run-time Critical Stop" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 C"Under-Temperature Warning (Lower non-critical, going high)Cleared"           �--#TYPE       "Temperature Event" 
--#SUMMARY    "Under-Temperature Warning (Lower non-critical, going high)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 8"Under-Current Warning (Lower non-critical, going high)"           �--#TYPE       "Current Event" 
--#SUMMARY    "Under-Current Warning (Lower non-critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 "Memory Scrub Failed"           r--#TYPE       "Memory Event" 
--#SUMMARY    "Memory Scrub Failed" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 /"Critical Interrupt, Bus Timeout error Cleared"           �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, Bus Timeout error Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "OS Watchdog Shut Down"           v--#TYPE       "Watchdog Event" 
--#SUMMARY    "OS Watchdog Shut Down" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 )"Network Boot Password Violation Attempt"           �--#TYPE       "Platform Securtiy Violation Attempt Event" 
--#SUMMARY    "Network boot Password Violation Attempt" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 7"Over-Current Warning (Upper non-critical, going high)"           �--#TYPE       "Current Event" 
--#SUMMARY    "Over-Current Warning (Upper non-critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 "SEL Full."           l--#TYPE       "System Event Log" 
--#SUMMARY    "SEL Full." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 L"Critical Under-Current problem (Lower non-recoverable, going high) Cleared"           �--#TYPE       "Current Event" 
--#SUMMARY    "Under-Current Warning (Lower non-recoverable, going high) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Secure Mode Violation Attempt"           �--#TYPE       "Platform Securtiy Violation Attempt Event" 
--#SUMMARY    "Secure Mode Violation Attempt" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 >"Critical Fan Over Speed problem (Upper critical, going high)"           �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Over Speed Warning (Upper critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 2"Memory Predictive Failure state has been cleared"           �--#TYPE       "Memory Event" 
--#SUMMARY    "Memory Predictive Failure state has been cleared." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 6"Over-Current Warning (Upper non-critical, going low)"           �--#TYPE       "Current Event" 
--#SUMMARY    "Over-Current Warning (Upper non-critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 0"OS Watchdog Expired, status only Event Cleared"           �--#TYPE       "Watchdog Event" 
--#SUMMARY    "OS Watchdog Expired, status only Event Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Add-in Card State Asserted"           ~--#TYPE       "Add-in Card Event" 
--#SUMMARY    "Add-in Card State Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 I"Critical Over-Current problem (Upper non-recoverable, going low)Cleared"           �--#TYPE       "Current Event" 
--#SUMMARY    "Over-Current Warning (Upper non-recoverable, going low)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Thermal Trip Cleared"           u--#TYPE       "Chip Set Event" 
--#SUMMARY    "Thermal Trip Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 W"Processor Fault Resilient Booting (FRB) 2 / Hang in Power On Self Test (POST) Failure"           �--#TYPE       "Processor Event" 
--#SUMMARY    "Processor Fault Resilient Booting (FRB) 2 / Hang in Power On Self Test (POST) Failure" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL  
 C"Critical Over-Voltage problem (Upper non-recoverable, going high)"           �--#TYPE       "Voltage Event" 
--#SUMMARY    "Under-Voltage Warning (Upper non-recoverable, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 J"Critical Under-Current problem (Lower non-recoverable, going low)Cleared"           �--#TYPE       "Current Event" 
--#SUMMARY    "Under-Current Warning (Lower non-recoverable, going low)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "FRU State Asserted"           t--#TYPE       "Other FRU Event" 
--#SUMMARY    "FRU State Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 0"Front Panel NMI / Diagnostic Interrupt Cleared"           �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Front Panel NMI / Diagnostic Interrupt Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 D"Critical Fan Over Speed problem (Upper non-recoverable, going low)"           �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Over Speed Warning (Upper non-recoverable, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 G"FRU latch Closed (Switch indicating FRU latch is in latched position)"           v--#TYPE       "Button/Switch Event" 
--#SUMMARY    "FRU latch Closed" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 E"Critical Under-Voltage problem (Lower critical, going high) Cleared"           �--#TYPE       "Voltage Event" 
--#SUMMARY    "Under-Voltage Warning (Lower critical, going high) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 8"Under-Voltage Warning (Lower non-critical, going high)"           �--#TYPE       "Voltage Event" 
--#SUMMARY    "Under-Voltage Warning (Lower non-critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 "Session Activated"           w--#TYPE       "Session Audit Event" 
--#SUMMARY    "Session Activated" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 M"Critical Over-Temperature problem (Upper non-recoverable, going low)Cleared"           �--#TYPE       "Temperature Event" 
--#SUMMARY    "Over-Temperature Warning (Upper non-recoverable, going low)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 P"Generic Critical Temperature Problem (Transition to Critical from less severe)"           �--#TYPE       "Temperature Event" 
--#SUMMARY    "Generic Critical Temperature Problem (Transition to Critical from less severe)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 7"Over-Voltage Warning (Upper non-critical, going high)"           �--#TYPE       "Voltage Event" 
--#SUMMARY    "Over-Voltage Warning (Upper non-critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 B"Over-Temperature Warning (Upper non-critical, going high)Cleared"           �--#TYPE       "Temperature Event" 
--#SUMMARY    "Over-Temperature Warning (Upper non-critical, going high)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Power Unit Failure detected"           ~--#TYPE       "Power unit event" 
--#SUMMARY    "Power Unit Failure detected" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Power Supply AC Lost"           t--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply AC Lost" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 K"This state indicates that a HDD Fault LED which was ON before is OFF now."           �--#TYPE       "Drive Slot Event" 
--#SUMMARY    "Hard Disk Drive Fault LED is OFF." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 %"Critical Interrupt, Fatal NMI error"           �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, Fatal NMI error" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 C"Critical Over-Current problem (Upper critical, going low) Cleared"           �--#TYPE       "Current Event" 
--#SUMMARY    "Over-Current Warning (Upper critical, going low) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Power Button Released."           |--#TYPE       "Button/Switch Event" 
--#SUMMARY    "Power Button Released." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Power Supply Warning Cleared"           �--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply Warning Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 L"Generic Critical Voltage Problem (Transition to Critical from less severe)"           �--#TYPE	      "Voltage Event" 
--#SUMMARY    "Generic Critical Voltage Problem (Transition to Critical from less severe)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "PXE Server found"           s--#TYPE       "Boot Error Event" 
--#SUMMARY    "PXE Server found" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ""SEL Entry added to Auxiliary Log"           --#TYPE       "System Event" 
--#SUMMARY    "SEL Entry added to Auxiliary Log" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 8"Critical Interrupt, IO Channel check NMI error Cleared"           �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, IO Channel check NMI error Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Hard Disk Drive Fault Cleared"           �--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive Fault Cleared" 
--#ARGUMENTS    {} 
--#SEVERITY     INFORMATIONAL 
 )"SM BIOS Uncorrectable CPU-complex Error"           �--#TYPE       "Processor Event" 
--#SUMMARY    "SM BIOS Uncorrectable CPU-complex Error" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 !"I/O Card Area Intrusion Cleared"           �--#TYPE       "Chassis Intrusion Event" 
--#SUMMARY    "I/O Card Area Intrusion Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 +"Correctable Memory Error Logging Disabled"           �--#TYPE       "System Event Log" 
--#SUMMARY    "Correctable Memory Error Logging Disabled" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
  "Watchdog Power Down Deasserted"           z--#TYPE       "Watchdog Event" 
--#SUMMARY    "Watchdog Power Down Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 E"Cooling Device Under Speed Warning (Lower non-critical, going high)"           �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Under Speed Warning (Lower non-critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 @"Boot Error - Timeout waiting for user selection of boot source"           �--#TYPE       "Boot Error Event" 
--#SUMMARY    "Boot Error - Timeout waiting for user selection of boot source" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 %"FRU service request button Released"           �--#TYPE       "Button/Switch Event" 
--#SUMMARY    "FRU service request button Released" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 *"Power Supply input out-of-range restored"           �--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply input out-of-range restored" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 @"Critical Over-Temperature problem (Upper critical, going high)"           �--#TYPE       "Temperature Event" 
--#SUMMARY    "Over-Temperature Warning (Upper critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "Session Deactivated"           s--#TYPE       "Session Audit Event" 
--#SUMMARY    "Session Deactivated" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 C"PEF Action is about to be taken. Event filters have been matched."           �--#TYPE       "System Event" 
--#SUMMARY    "PEF Action is about to be taken. Event filters have been matched." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 B"Critical Over-Voltage problem (Upper non-recoverable, going low)"           �--#TYPE       "Voltage Event" 
--#SUMMARY    "Over-Voltage Warning (Upper non-recoverable, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 C"Critical Over-Voltage problem (Upper critical, going low) Cleared"           �--#TYPE       "Voltage Event" 
--#SUMMARY    "Over-Voltage Warning (Upper critical, going low) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 %"Chassis Predictive Failure Asserted"           �--#TYPE       "Chassis Event" 
--#SUMMARY    "Chassis Predictive Failure Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ^"Processor Fault Resilient Booting (FRB) 3 / Processor Setup / Initialization Failure Cleared"           �--#TYPE	"Processor Event" 
--#SUMMARY    "Processor Fault Resilient Booting (FRB) 3 / Processor Setup / Initialization Failure Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 3"Memory Predictive Failure state has been asserted"           �--#TYPE       "Memory Event" 
--#SUMMARY    "Memory Predictive Failure has been asserted." 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 3"Critical Interrupt, Bus Correctable Error Cleared"           �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, Bus Correctable Error Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 C"Critical Over-Voltage problem (Upper critical, going high)Cleared"           �--#TYPE       "Voltage Event" 
--#SUMMARY    "Over-Voltage Warning (Upper critical, going high)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Power Supply Inserted"           z--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply Inserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 <"Critical Over-Voltage problem (Upper critical, going high)"           �--#TYPE       "Voltage Event" 
--#SUMMARY    "Over-Voltage Warning (Upper critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "Slot / Connector - Disabled"           �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Disabled" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Reset Button Released."           |--#TYPE       "Button/Switch Event" 
--#SUMMARY    "Reset Button Released." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 *"Correctable Memory Error Logging Enabled"           �--#TYPE       "System Event Log" 
--#SUMMARY    "Correctable Memory Error Logging Enabled" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 -"Slot / Connector - Identify Status asserted"           �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Identify Status asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ,"Critical Interrupt, EISA Fail Safe Timeout"           �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, EISA Fail Safe Timeout" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 L"Cooling Device Under Speed Warning (Lower non-critical, going low) Cleared"           �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Under Speed Warning (Lower non-critical, going low) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Watchdog Power Down"           o--#TYPE       "Watchdog Event" 
--#SUMMARY    "Watchdog Power Down" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 O"Processor Fault Resilient Booting (FRB) 1 / BIST (Built In Self Test) Failure"           �--#TYPE       "Processor Event" 
--#SUMMARY    "Processor Fault Resilient Booting (FRB) 1 / Processor BIST (Built In Self Test) Failure" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 8"System Boot / Restart Initiated by power up Deasserted"           �--#TYPE       "System Boot / Restart Event" 
--#SUMMARY    "System Boot / Restart Initiated by power up Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ,"Slot / Connector - Fault Status Deasserted"           �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Fault Status Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 $"Soft Power Control Failure Cleared"           �--#TYPE       "Power unit event" 
--#SUMMARY    "Soft Power Control Failure Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 F"Critical Fan Under Speed problem (Lower non-recoverable, going high)"           �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Under Speed Warning (Lower non-recoverable, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "Terminator Presence Detected"           ~--#TYPE       "Processor Event" 
--#SUMMARY    "Terminator Presence Detected" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ""CPU0 Channel0 Dimm2 memory Error"             L"Generic Critical Voltage Problem (Transition to Critical from less severe)"           �--#TYPE       "Voltage Event" 
--#SUMMARY    "Generic Critical Voltage Problem (Transition to Critical from less severe)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 ""CPU0 Channel0 Dimm1 memory Error"             ""CPU0 Channel0 Dimm0 memory Error"             9"Hardware Version change detected with associated Entity"           �--#TYPE       "Version Change Event" 
--#SUMMARY    "Hardware Version change detected" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 !"Watchdog Power Cycle Deasserted"           z--#TYPE       "Watchdog Event" 
--#SUMMARY    "Watchdog Power cycle Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 "FRU Activation In Progress"           |--#TYPE       "FRU State Event" 
--#SUMMARY    "FRU Activation In Progress" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 )"Add-in Card Predictive Failure Asserted"           �--#TYPE       "Add-in Card Event" 
--#SUMMARY    "Add-in Card Predictive Failure Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 )"Chassis Intrusion - Drive Bay Violation"           �--#TYPE       "Chassis Intrusion Event" 
--#SUMMARY    "Chassis Intrusion - Drive Bay Violation" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 :"System Boot / Restart Initiated by Warm Reset Deasserted"           �--#TYPE       "System Boot / Restart Event" 
--#SUMMARY    "System Boot / Restart Initiated by Warm Reset Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 8"Host power-on sequence has been completed successfully"           �--#TYPE         "Power Unit Event" 
--#SUMMARY      "Host power-on sequence has been completed successfully." 
--#ARGUMENTS    {} 
--#SEVERITY     INFORMATIONAL 
 %"Cable / Interconnect State Asserted"           �--#TYPE       "Other Cable / Interconnect Event" 
--#SUMMARY    "Cable / Interconnect State Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ."Hard Disk Drive In Critical Array Deasserted"           �--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive In Critical Array Deasserted" 
--#ARGUMENTS    {} 
--#SEVERITY     INFORMATIONAL 
 b"Slot / Connector - Not Ready for Device Removal. Typically, this means that the slot power is on"           �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Ready for Device Removal" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "FRU State Deasserted"           v--#TYPE       "Other FRU Event" 
--#SUMMARY    "FRU State Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 1"Network Boot Password Violation Attempt Cleared"           �--#TYPE       "Platform Securtiy Violation Attempt Event" 
--#SUMMARY    "Network boot Password Violation Attempt Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 1"Correctable Machine Check Error Logging Enabled"           �--#TYPE       "System Event Log" 
--#SUMMARY    "Correctable Machine Check Error Logging Enabled" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 _"Processor Fault Resilient Booting (FRB) 2 / Hang in Power On Self Test (POST) Failure Cleared"           �--#TYPE       "Processor Event" 
--#SUMMARY    "Processor Fault Resilient Booting (FRB) 2 / Hang in Power On Self Test (POST) Failure Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL  
 A"System Boot / Restart - Automatic boot to diagnostic Deasserted"           �--#TYPE       "System Boot / Restart Event" 
--#SUMMARY    "System Boot / Restart - Automatic boot to diagnostic Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 J"Chip Set started responding to BMC request to change system power state."           �--#TYPE       "Chip Set Event" 
--#SUMMARY    "Soft Power Control Failure Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 /"System Boot / Restart Initiated by Warm Reset"           �--#TYPE       "System Boot / Restart Event" 
--#SUMMARY    "System Boot / Restart Initiated by Warm Reset" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 +"A device is present or has been inserted."           �--#TYPE       "Entity Presence Event" 
--#SUMMARY    "A device is present or has been inserted." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ="Critical Under-Current problem (Lower critical, going high)"           �--#TYPE       "Current Event" 
--#SUMMARY    "Under-Current Warning (Lower critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 -"Critical Interrupt, Bus Uncorrectable error"           �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, Bus Uncorrectable error" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 2"Power Supply input lost or out-of-range Restored"           �--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply input lost or out-of-range Restored" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 B"The Entity identified by the Entity ID for the sensor is Absent."           v--#TYPE       "Entity Presence Event" 
--#SUMMARY    "Entity Absent." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 -"Critical Interrupt, Bus Fatal Error Cleared"           �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, Bus Fatal Error Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 X"Critical Cooling Device Over Speed problem (Upper non-recoverable, going high) Cleared"           �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Under Speed Warning (Upper non-recoverable, going high) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 )"User Password Violation Attempt Cleared"           �--#TYPE       "Platform Securtiy Violation Attempt Event" 
--#SUMMARY    "User Password Violation Attempt Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "ROM boot completed"           r--#TYPE       "OS Boot Event" 
--#SUMMARY    "ROM boot completed" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 4"Processor Thermal Trip (Over Temperature Shutdown)"           �--#TYPE       "Processor Event" 
--#SUMMARY    "Processor Thermal Trip (Over Temperature Shutdown)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 _"Slot / Connector - Ready for Device Removal. Typically, this means that the slot power is off"           �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Ready for Device Removal" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 `"OS Stop / Shutdown - System powered up by reset pushbutton, powercycle or other external input"           �--#TYPE       "OS Stop / Shutdown Event" 
--#SUMMARY    "OS Stop / Shutdown - Graceful Stop Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Sensor failure Deasserted"           �--#TYPE       "Management Subsystem Health Event" 
--#SUMMARY    "Sensor failure Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 A"Uncorrectable ECC or other uncorrectable memory error detected."           �--#TYPE       "Memory Event" 
--#SUMMARY    "Uncorrectable ECC or other uncorrectable memory error detected." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 *"Slot / Connector - Fault Status asserted"           �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Fault Status asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Sensor failure"           z--#TYPE       "Management Subsystem Health Event" 
--#SUMMARY    "Sensor failure" 
--#ARGUMENTS  {} 
--#SEVERITY   MAJOR 
 ,"Power Supply Predictive Failure Deasserted"           �--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply Predictive Failure Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 ."Slot / Connector - Device installed/attached"           �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Device installed/attached" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 D"Hardware Change detected with associated Entity was not successful"           �--#TYPE       "Version Change Event" 
--#SUMMARY    "Hardware Change detected with associated Entity was not successful" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 D"Critical Under-Voltage problem (Lower non-recoverable, going high)"           �--#TYPE       "Voltage Event" 
--#SUMMARY    "Under-Voltage Warning (Lower non-recoverable, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 -"System Boot / Restart Initiated by power up"           �--#TYPE       "System Boot / Restart Event" 
--#SUMMARY    "System Boot / Restart Initiated by power up" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Battery low"           e--#TYPE       "Battery Event" 
--#SUMMARY    "Battery low" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 -"Critical Interrupt, Fatal NMI error Cleared"           �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, Fatal NMI error Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 E"System Boot / Restart - OS / run-time software initiated Warm reset"           �--#TYPE       "System Boot / Restart Event" 
--#SUMMARY    "System Boot / Restart - OS / run-time software initiated Warm reset" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "FRU service request button"           �--#TYPE       "Button/Switch Event" 
--#SUMMARY    "FRU service request button" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Power Button pressed."           {--#TYPE       "Button/Switch Event" 
--#SUMMARY    "Power Button pressed." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 >"Over-Voltage Warning (Upper non-critical, going high)Cleared"           �--#TYPE       "Voltage Event" 
--#SUMMARY    "Over-Voltage Warning (Upper non-critical, going high)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ?"Under-Current Warning (Lower non-critical, going low) Cleared"           �--#TYPE       "Current Event" 
--#SUMMARY    "Under-Current Warning (Lower non-critical, going low) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 !"FRU Predictive Failure Asserted"           �--#TYPE       "Other FRU Event" 
--#SUMMARY    "FRU Predictive Failure Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "OS Watchdog Reset"           r--#TYPE       "Watchdog Event" 
--#SUMMARY    "OS Watchdog Reset" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Power unit is power cycled"           }--#TYPE       "Power unit event" 
--#SUMMARY    "Power unit is power cycled" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 C"Critical Under-Current problem (Lower critical, going low)Cleared"           �--#TYPE       "Current Event" 
--#SUMMARY    "Under-Current Warning (Lower critical, going low)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 7"Under-Current Warning (Lower non-critical, going low)"           �--#TYPE       "Current Event" 
--#SUMMARY    "Under-Current Warning (Lower non-critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 "Found valid boot sector"           z--#TYPE       "Boot Error Event" 
--#SUMMARY    "Found Valid boot sector" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ""Processor Internal Error Cleared"           �--#TYPE       "Processor Event" 
--#SUMMARY    "Processor Internal Error Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 M"Configuration Error - Incorrect cable connected / Incorrect interconnection"           �--#TYPE       "Other Cable / Interconnect Event" 
--#SUMMARY    "Configuration Error" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 0"Platform Alert - Platform Event Trap generated"           �--#TYPE       "Platform Alert Event" 
--#SUMMARY    "Platform Alert-  Platform Event Trap generated (formatted per IPMI PET specification)" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Soft Power Control Failure"           }--#TYPE       "Power unit event" 
--#SUMMARY    "Soft Power Control Failure" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 )"Power Unit Redundancy has been restored"           �--#TYPE       "Power Unit Event" 
--#SUMMARY    "Power Unit Redundancy has been restored" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Parity error Cleared."           t--#TYPE       "Memory Event" 
--#SUMMARY    "Parity error Cleared." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 N"Firmware Or Software Version Incompatibility detected with associated Entity"           �--#TYPE       "Version Change Event" 
--#SUMMARY    "Firmware Or SoftwareVersion Incompatibility detected" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Management controller online"           �--#TYPE       "Management Subsystem Health Event" 
--#SUMMARY    "Management controller online" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 0"Hard Disk Drive is absent or has been removed."           �--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive is absent or has been removed." 
--#ARGUMENTS    {} 
--#SEVERITY     INFORMATIONAL 
 ,"OS Stop / Shutdown -Power Cycle/Reset Done"           �--#TYPE       "OS Stop / Shutdown Event" 
--#SUMMARY    "OS Stop / Shutdown - Run-time INFORMATIONAL Stop Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 P"Critical Cooling Device Over Speed problem (Upper critical, going high)Cleared"           �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Over Speed Warning (Upper critical, going high)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Memory Device Disabled."           v--#TYPE       "Memory Event" 
--#SUMMARY    "Memory Device Disabled." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 $"Cable/Interconnect is disconnected"           �--#TYPE       "Other Cable / Interconnect Event" 
--#SUMMARY    "Cable/Interconnect is disconnected" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 2"Cable / Interconnect Predictive Failure Asserted"           �--#TYPE       "Other Cable / Interconnect Event" 
--#SUMMARY    "Cable / Interconnect Predictive Failure Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 P"Critical Cooling Device Under Speed problem (Lower non-recoverable, going low)"           �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Under Speed Warning (Lower non-recoverable, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 G"Generic Voltage Warning (Transition to Non-Critical from more severe)"           �--#TYPE	      "Voltage Event" 
--#SUMMARY    "Generic Voltage Warning (Transition to Non-Critical from more severe)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 -"OS Stop / Shutdown - power cycle/reset Done"           �--#TYPE       "OS Stop / Shutdown Event" 
--#SUMMARY    "OS Stop / Shutdown - Stop during OS load / initialization Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 Y"Critical Cooling Device Under Speed problem (Lower non-recoverable, going high) Cleared"           �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Under Speed Warning (Lower non-recoverable, going high) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ;"Under-Temperature Warning (Lower non-critical, going low)"           �--#TYPE       "Temperature Event" 
--#SUMMARY    "Under-Temperature Warning (Lower non-critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 +"Other Pre-boot Password Violation Attempt"           �--#TYPE       "Platform Securtiy Violation Attempt Event" 
--#SUMMARY    "Other pre-boot Password Violation Attempt" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 E"System Boot / Restart - OS / run-time software initiated hard reset"           �--#TYPE       "System Boot / Restart Event" 
--#SUMMARY    "System Boot / Restart - OS / run-time software initiated hard reset" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 !"Power unit Interlock Power Down"           �--#TYPE       "Power unit event" 
--#SUMMARY    "Power unit Interlock Power Down" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ""Power Supply Configuration error"           �--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply Configuration error" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 L"System Boot / Restart - Restart cause per Get System Restart Cause command"           �--#TYPE       "System Boot / Restart Event" 
--#SUMMARY    "System Boot / Restart - Restart cause per Get System Restart Cause command" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 %"Slot / Connector - Slot Power is On"           �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Slot Power is On" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 +"Slot / Connector - Device Removal Request"           �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Device Removal Request" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 1"Chassis Intrusion - Physical Security Violation"           �--#TYPE       "Chassis Intrusion Event" 
--#SUMMARY    "Chassis Intrusion - Physical Security Violation" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 !"Cooling Device Inserted/Present"           �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Inserted/Present" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 %"Critical Interrupt, Bus Fatal Error"           �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, Bus Fatal Error" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 0"System Firmware Progress: BIOS POST code error"           �--#TYPE       "System Firmware Progress Event" 
--#SUMMARY    "System Firmware Progress: BIOS POST code error" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 P"Correctable ECC / other correctable memory error logging limit reached Cleared"           �--#TYPE       "Memory Event" 
--#SUMMARY    "Correctable ECC / other correctable memory error logging limit reached Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "test"           �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Under Speed Warning (Upper non-recoverable, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "Power supply Failure detected"           }--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply failure detected" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 /"Slot / Connector - Device Uninstalled/Removed"           �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Device Uninstalled/Removed" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 -"SEL Entry added to Auxiliary Log Deasserted"           �--#TYPE       "System Event" 
--#SUMMARY    "SEL Entry added to Auxiliary Log Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "PXE boot Incomplete"           m--#TYPE       "OS Boot Event" 
--#SUMMARY    "PXE boot Incomplete" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 "Event Type Logging Enabled"           ~--#TYPE       "System Event Log" 
--#SUMMARY    "Event Type Logging Enabled." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 <"Correctable ECC or other correctable memory error cleared."           �--#TYPE       "Memory Event" 
--#SUMMARY    "Correctable ECC or other correctable memory error cleared." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 +"Critical Interrupt, PCI PERR parity error"           �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, PCI PERR parity error" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 D"The Entity identified by the Entity ID for the sensor is Disabled."           x--#TYPE       "Entity Presence Event" 
--#SUMMARY    "Entity Disabled." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 C"Critical Over-Current problem (Upper non-recoverable, going high)"           �--#TYPE       "Current Event" 
--#SUMMARY    "Under-Current Warning (Upper non-recoverable, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 N"Critical Fan Under Speed problem (Lower non-recoverable, going high) Cleared"           �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Under Speed Warning (Lower non-recoverable, going high) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ="Critical Under-Voltage problem (Lower critical, going high)"           �--#TYPE       "Voltage Event" 
--#SUMMARY    "Under-Voltage Warning (Lower critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "OS Watchdog Reset Deasserted"           }--#TYPE       "Watchdog Event" 
--#SUMMARY    "OS Watchdog Reset Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Memory Scrub Failure Cleared"           {--#TYPE       "Memory Event" 
--#SUMMARY    "Memory Scrub Failure Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 >"Hard Disk Drive Consistency Check / Parity Check in progress"           �--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive Consistency Check / Parity Check in progress" 
--#ARGUMENTS    {} 
--#SEVERITY     INFORMATIONAL 
 I"Hard Disk Drive Consistency Check / Parity Check in progress Deasserted"           �--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive Consistency Check / Parity Check in progress Deasserted" 
--#ARGUMENTS    {} 
--#SEVERITY     INFORMATIONAL 
 "FRU Deactivation In Progress"           ~--#TYPE       "FRU State Event" 
--#SUMMARY    "FRU Deactivation In Progress" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 &"Session Invalid Username or Password"           �--#TYPE       "Session Audit Event" 
--#SUMMARY    "Session Invalid Username or Password" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 "Power Unit is on."           t--#TYPE       "Power Unit event" 
--#SUMMARY    "Power Unit is on." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ("Timestamp Clock Synch Event Deasserted"           �--#TYPE       "System Event" 
--#SUMMARY    "Timestamp Clock Synch Event Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 P"Critical Cooling Device Over Speed problem (Upper non-recoverable, going high)"           �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Under Speed Warning (Upper non-recoverable, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 A"Fan Under Speed Warning (Lower non-critical, going high)Cleared"           �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Under Speed Warning (Lower non-critical, going high)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Battery Failed"           i--#TYPE       "Battery Event" 
--#SUMMARY    "Battery Failed" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 *"Module/Board Predictive Failure Asserted"           �--#TYPE       "Module/Board Event" 
--#SUMMARY    "Module/Board Predictive Failure Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 C"Critical Over-Current problem (Upper critical, going high)Cleared"           �--#TYPE       "Current Event" 
--#SUMMARY    "Over-Current Warning (Upper critical, going high)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "SEL Almost Full."           s--#TYPE       "System Event Log" 
--#SUMMARY    "SEL Almost Full." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "OEM System Boot Event"           n--#TYPE       "System Event" 
--#SUMMARY    "OEM System Boot Event" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 )"Slot / Connector - Interlock Deasserted"           �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Interlock Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 '"Sensor access degraded or unavailable"           �--#TYPE       "Management Subsystem Health Event" 
--#SUMMARY    "Sensor access degraded or unavailable" 
--#ARGUMENTS  {} 
--#SEVERITY   MAJOR 
 5"Slot / Connector - Device Removal Request Processed"           �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Device Removal Request Processed" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 I"Critical Cooling Device Over Speed problem (Upper critical, going high)"           �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Over Speed Warning (Upper critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "CDROM boot Incomplete"           o--#TYPE       "OS Boot Event" 
--#SUMMARY    "CDROM boot Incomplete" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 ."Out-of-band access Violation Attempt Cleared"           �--#TYPE       "Platform Securtiy Violation Attempt Event" 
--#SUMMARY    "Out-of-band access Violation Attempt Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Processor Internal Error"           u--#TYPE       "Processor Event" 
--#SUMMARY    "Processor Internal Error" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 2"Correctable Machine Check Error Logging Disabled"           �--#TYPE       "System Event Log" 
--#SUMMARY    "Correctable Machine Check Error Logging Disabled" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 *"Terminator Predictive Failure Deasserted"           �--#TYPE       "Terminator Event" 
--#SUMMARY    "Terminator Predictive Failure Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 &"Undetermined system hardware failure"           ~--#TYPE       "System Event" 
--#SUMMARY    "Undetermined system hardware failure" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "Power unit is off."           u--#TYPE       "Power unit event" 
--#SUMMARY    "Power unit is off." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "BIOS Watchdog Reset"           t--#TYPE       "Watchdog Event" 
--#SUMMARY    "BIOS Watchdog Reset" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 &"Hard Disk Drive Hot Spare Deasserted"           �--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive Hot spare" 
--#ARGUMENTS    {} 
--#SEVERITY     INFORMATIONAL 
 %"POST Memory Resize Failure Asserted"           �--#TYPE       "POST Memory Resize Event" 
--#SUMMARY    "POST Memory Resize Failure Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   MAJOR 
 @"Hardware Change detected with associated Entity was successful"           �--#TYPE       "Version Change Event" 
--#SUMMARY    "Hardware Change detected with associated Entity was successful" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 $"Monitor ASIC / IC Failure Asserted"           �--#TYPE       "Monitor ASIC / IC Event" 
--#SUMMARY    "Monitor ASIC / IC Failure Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   MAJOR 
 G"Critical Under-Temperature problem (Lower non-recoverable, going low)"           �--#TYPE       "Temperature Event" 
--#SUMMARY    "Under-Temperature Warning (Lower non-recoverable, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 C"Critical Under-Current problem (Lower non-recoverable, going low)"           �--#TYPE       "Current Event" 
--#SUMMARY    "Under-Current Warning (Lower non-recoverable, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 F"Critical Over-Temperature problem (Upper non-recoverable, going low)"           �--#TYPE       "Temperature Event" 
--#SUMMARY    "Over-Temperature Warning (Upper non-recoverable, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 9"Hardware Incombabaility detected with associated Entity"           �--#TYPE       "Version Change Event" 
--#SUMMARY    "Hardware Incombabaility detected" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 -"Power Supply is disconnected from AC Power."           �--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply is disconnected from AC Power." 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "Fan Redundancy has been Lost"           s--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Redundancy has been Lost" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "SEL Full Event Cleared"           y--#TYPE       "System Event Log" 
--#SUMMARY    "SEL Full Event Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 L"Critical Fan Under Speed problem (Lower non-recoverable, going low)Cleared"           �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Under Speed Warning (Lower non-recoverable, going low)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ""OS Watchdog Expired, status only"           �--#TYPE       "Watchdog Event" 
--#SUMMARY    "OS Watchdog Expired, status only" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "FRU Activation Requested"           z--#TYPE       "FRU State Event" 
--#SUMMARY    "FRU Activation Requested" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 P"Critical Cooling Device Over Speed problem (Upper critical, going low) Cleared"           �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Over Speed Warning (Upper critical, going low) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ?"Under-Voltage Warning (Lower non-critical, going high)Cleared"           �--#TYPE       "Voltage Event" 
--#SUMMARY    "Under-Voltage Warning (Lower non-critical, going high)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 2"System ACPI Power State - S5 entered by override"           �--#TYPE       "System ACPI Power State Event" 
--#SUMMARY    "System ACPI Power State - S5 entered by override" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ""Setup Password Violation Attempt"           �--#TYPE       "Platform Securtiy Violation Attempt Event" 
--#SUMMARY    "Setup Password Violation Attempt" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "Chassis State Deasserted"           x--#TYPE       "Chassis Event" 
--#SUMMARY    "Chassis State Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 3"Critical Interrupt, PCI PERR parity error Cleared"           �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, PCI PERR parity error Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ,"Boot completed - boot device not specified"           �--#TYPE       "OS Boot Event" 
--#SUMMARY    "Boot completed - boot device not specified" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "SEL Area Reset/Cleared"           �--#TYPE       "System Event Log" 
--#SUMMARY    "SEL Area Reset/Cleared Event Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 V"Processor Fault Resilient Booting (FRB) 3 / Processor Setup / Initialization Failure"           �--#TYPE	"Processor Event" 
--#SUMMARY    "Processor Fault Resilient Booting (FRB) 3 / Processor Setup / Initialization Failure" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 ."System ACPI Power State - S5 / G2 - soft-off"           �--#TYPE       "System ACPI Power State Event" 
--#SUMMARY    "System ACPI Power State - S5 / G2" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 P"System Boot / Restart - OS / run-time software initiated Warm reset Deasserted"           �--#TYPE       "System Boot / Restart Event" 
--#SUMMARY    "System Boot / Restart - OS / run-time software initiated Warm reset Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 E"System ACPI Power State - S4 - non-volatile sleep / suspend-to disk"           �--#TYPE       "System ACPI Power State Event" 
--#SUMMARY    "System ACPI Power State - S4" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "System ACPI Power State - S3"           �--#TYPE       "System ACPI Power State Event" 
--#SUMMARY    "System ACPI Power State - S3 - sleeping, processor & h/w context lost, memory retained" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ?"System ACPI Power State - S2 sleeping, processor context lost"           �--#TYPE       "System ACPI Power State Event" 
--#SUMMARY    "System ACPI Power State - S2 " 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 X"System ACPI Power State - S1 - sleeping with system h/w & processor context maintained"           �--#TYPE       "System ACPI Power State Event" 
--#SUMMARY    "System ACPI Power State - S1" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Power unit Interlock Power Up"           �--#TYPE       "Power unit event" 
--#SUMMARY    "Power unit Interlock Power Up" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "System Event Logging Enabled"           --#TYPE       "System Event Log" 
--#SUMMARY    "System Event Logging Enabled" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 Q"Critical Cooling Device Under Speed problem (Lower non-recoverable, going high)"           �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Under Speed Warning (Lower non-recoverable, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 ""Boot Error - Invalid boot sector"           ~--#TYPE       "Boot Error Event" 
--#SUMMARY    "Boot Error - Invalid boot sector" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "Parity error detected."           u--#TYPE       "Memory Event" 
--#SUMMARY    "Parity error detected." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 7"Under-Voltage Warning (Lower non-critical, going low)"           �--#TYPE       "Voltage Event" 
--#SUMMARY    "Under-Voltage Warning (Lower non-critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 -"System ACPI Power State - S0 / G0 - Working"           �--#TYPE       "System ACPI Power State Event" 
--#SUMMARY    "System ACPI Power State - S0 / G0 " 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "FRU Not Installed"           s--#TYPE       "FRU State Event" 
--#SUMMARY    "FRU Not Installed" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Hard Disk Drive Fault"           {--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive Fault" 
--#ARGUMENTS    {} 
--#SEVERITY     CRITICAL 
 ?"System ACPI Power State - Sleeping in an S1, S2, or S3 states"           �--#TYPE       "System ACPI Power State Event" 
--#SUMMARY    "System ACPI Power State - Sleeping in an S1, S2, or S3 states" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 '"Power Supply Redundancy has been Lost"           �--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply Redundancy has been Lost" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 '"Power unit AC lost / Power input lost"           �--#TYPE       "Power unit event" 
--#SUMMARY    "Power unit AC lost / Power input lost" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 8"System Firmware Progress: BIOS POST code error Cleared"           �--#TYPE       "System Firmware Progress Event" 
--#SUMMARY    "System Firmware Progress: BIOS POST code error Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 #"System ACPI Power State - Unknown"           �--#TYPE       "System ACPI Power State Event" 
--#SUMMARY    "System ACPI Power State - Unknown" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "FRU failure Deasserted"           �--#TYPE       "Management Subsystem Health Event" 
--#SUMMARY    "FRU failure Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 G"Chip Set did not respond to BMC request to change system power state."           u--#TYPE       "Chip Set Event" 
--#SUMMARY    "Soft Power Control Failure" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 R"Critical Interrupt, Bus Degraded (bus operating in a degraded performance state)"           �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, Bus Degraded (bus operating in a degraded performance state)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "Power Unit Failure Cleared"           }--#TYPE       "Power unit event" 
--#SUMMARY    "Power Unit Failure Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Battery presence detected"           y--#TYPE       "Battery Event" 
--#SUMMARY    "Battery presence detected" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "C: boot completed"           q--#TYPE       "OS Boot Event" 
--#SUMMARY    "C: boot completed" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 L"A user's access has been disabled due to a series of bad password attempts"           �--#TYPE       "Session Audit Event" 
--#SUMMARY    "Session Invalid password disable" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 "A: boot completed"           q--#TYPE       "OS Boot Event" 
--#SUMMARY    "A: boot completed" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 A"Fan Under Speed Warning (Lower non-critical, going low) Cleared"           �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Under Speed Warning (Lower non-critical, going low) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 '"Secure Mode Violation Attempt Cleared"           �--#TYPE       "Platform Securtiy Violation Attempt Event" 
--#SUMMARY    "Secure Mode Violation Attempt Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 <"Processor Thermal Trip (Over Temperature Shutdown) Cleared"           �--#TYPE       "Processor Event" 
--#SUMMARY    "Processor Thermal Trip (Over Temperature Shutdown) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 9"Generic Voltage Warning (Transition to Non-Recoverable)"           �--#TYPE	      "Voltage Event" 
--#SUMMARY    "Generic Voltage Warning (Transition to Non-Recoverable)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 0"Power Supply Redundancy is in a degraded state"           �--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply Redundancy is in a degraded state" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 ("Memory Automatically Throttled Cleared"           �--#TYPE       "Memory Event" 
--#SUMMARY    "Memory Automatically Throttled Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 E"Firmware or Software version change detected with associated Entity"           �--#TYPE       "Version Change Event" 
--#SUMMARY    "Firmware or Software version change detected" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 #"Hard Disk Drive In Critical Array"           �--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive In Critical Array" 
--#ARGUMENTS    {} 
--#SEVERITY     INFORMATIONAL 
 :"Over-Temperature Warning (Upper non-critical, going low)"           �--#TYPE       "Temperature Event" 
--#SUMMARY    "Over-Temperature Warning (Upper non-critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 D"Critical Under-Current problem (Lower non-recoverable, going high)"           �--#TYPE       "Current Event" 
--#SUMMARY    "Under-Current Warning (Lower non-recoverable, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "Terminator State Asserted"           |--#TYPE       "Terminator Event" 
--#SUMMARY    "Terminator State Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Power supply Warning"           s--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply Warning" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 )"Cooling Device Redundancy has been Lost"           �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Redundancy has been Lost" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 i"FRU latch open (Switch indicating FRU latch is in unlatched position and FRU is mechanically removable)"           t--#TYPE       "Button/Switch Event" 
--#SUMMARY    "FRU latch open" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "System Firmware Progress"           �--#TYPE       "System Firmware Progress Event" 
--#SUMMARY    "System Firmware Progress" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Timestamp Clock Synch"           t--#TYPE       "System Event" 
--#SUMMARY    "Timestamp Clock Synch" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 >"Over-Current Warning (Upper non-critical, going high)Cleared"           �--#TYPE       "Current Event" 
--#SUMMARY    "Over-Current Warning (Upper non-critical, going high)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Sensor access Available"           �--#TYPE       "Management Subsystem Health Event" 
--#SUMMARY    "Sensor access Available" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Configuration Error Cleared"           �--#TYPE       "Other Cable / Interconnect Event" 
--#SUMMARY    "Configuration Error Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 !"Cable/Interconnect is connected"           �--#TYPE       "Other Cable / Interconnect Event" 
--#SUMMARY    "Cable/Interconnect is connected" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 5"Critical Interrupt, Bus Uncorrectable error Cleared"           �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, Bus Uncorrectable error Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 /"Platform Alert - platform generated LAN alert"           �--#TYPE       "Platform Alert Event" 
--#SUMMARY    "Platform Alert- platform generated LAN alert" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "LAN Leash Lost"           s--#TYPE       "Chassis Intrusion Event" 
--#SUMMARY    "LAN Leash Lost" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 K"Cooling Device Over Speed Warning (Upper non-critical, going high)Cleared"           �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Over Speed Warning (Upper non-critical, going high)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 P"Critical Cooling Device Under Speed problem (Lower critical, going low)Cleared"           �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Under Speed Warning (Lower critical, going low)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Cooling Device Removed/Absent"           --#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Removed/Absent" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 &"Out-of-band access Violation Attempt"           �--#TYPE       "Platform Securtiy Violation Attempt Event" 
--#SUMMARY    "Out-of-band access Violation Attempt" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "Memory Presence Not detected"           {--#TYPE       "Memory Event" 
--#SUMMARY    "Memory Presence not detected" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Slot / Connector - Enabled"           �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Enabled" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 '"Cable / Interconnect State Deasserted"           �--#TYPE       "Other Cable / Interconnect Event" 
--#SUMMARY    "Cable / Interconnect State Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 #"FRU Predictive Failure Deasserted"           �--#TYPE       "Other FRU Event" 
--#SUMMARY    "FRU Predictive Failure Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 C"Under-Temperature Warning (Lower non-critical, going low) Cleared"           �--#TYPE       "Temperature Event" 
--#SUMMARY    "Under-Temperature Warning (Lower non-critical, going low) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Power Supply Removed"           s--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply Removed" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 B"Over-Temperature Warning (Upper non-critical, going low) Cleared"           �--#TYPE       "Temperature Event" 
--#SUMMARY    "Over-Temperature Warning (Upper non-critical, going low) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 /"System Boot / Restart Initiated by Hard Reset"           �--#TYPE       "System Boot / Restart Event" 
--#SUMMARY    "System Boot / Restart Initiated by Hard Reset" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 $"Power unit - Power Cycle Completed"           �--#TYPE       "Power unit event" 
--#SUMMARY    "Power unit - Power Cycle Completed" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "FRU failure"           w--#TYPE       "Management Subsystem Health Event" 
--#SUMMARY    "FRU failure" 
--#ARGUMENTS  {} 
--#SEVERITY   MAJOR 
 ("Front Panel NMI / Diagnostic Interrupt"           �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Front Panel NMI / Diagnostic Interrupt" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 ."Microcontroller/Coprocessor State Deasserted"           �--#TYPE       "Microcontroller/Coprocessor Event" 
--#SUMMARY    "Microcontroller/Coprocessor State Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
  "Memory Automatically Throttled"           }--#TYPE       "Memory Event" 
--#SUMMARY    "Memory Automatically Throttled" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 2"Boot Error - Non-bootable diskette left in drive"           �--#TYPE       "Boot Error Event" 
--#SUMMARY    "Boot Error - Non-bootable diskette left in drive" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 #"Management controller Unavailable"           �--#TYPE       "Management Subsystem Health Event" 
--#SUMMARY    "Management controller Unavailable" 
--#ARGUMENTS  {} 
--#SEVERITY   MAJOR 
  "Boot Error - No bootable media"           |--#TYPE       "Boot Error Event" 
--#SUMMARY    "Boot Error - No bootable media" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 '"Fan redundancy has returned to Normal"           �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan redundancy has returned to Normal" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 %"Power Unit Redundancy has been Lost"           �--#TYPE       "Power Unit Event" 
--#SUMMARY    "Power Unit Redundancy has been Lost" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 O"Critical Over-Temperature problem (Upper non-recoverable, going high) Cleared"           �--#TYPE       "Temperature Event" 
--#SUMMARY    "Under-Temperature Warning (Upper non-recoverable, going high) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 /"Slot / Connector - Identify Status Deasserted"           �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Identify Status Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Add-in Card State Deasserted"           �--#TYPE       "Add-in Card Event" 
--#SUMMARY    "Add-in Card State Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 #"OS Watchdog Power Down Deasserted"           �--#TYPE       "Watchdog Event" 
--#SUMMARY    "OS Watchdog Power Down Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 5"Processor Throttle Cleared (Normal Processor Speed)"           �--#TYPE       "Processor Event" 
--#SUMMARY    "Processor Throttle Cleared (Normal Processor Speed)" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 +"System ACPI Power State - Legacy ON state"           �--#TYPE       "System ACPI Power State Event" 
--#SUMMARY    "System ACPI Power State - Legacy ON state" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 E"Critical Under-Current problem (Lower critical, going high) Cleared"           �--#TYPE       "Current Event" 
--#SUMMARY    "Under-Current Warning (Lower critical, going high) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 D"Cooling Device Under Speed Warning (Lower non-critical, going low)"           �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Under Speed Warning (Lower non-critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 "Fan Removed/Absent"           i--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Removed/Absent" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "Memory Device Enabled."           u--#TYPE       "Memory Event" 
--#SUMMARY    "Memory Device Enabled." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 !"Management controller Available"           �--#TYPE       "Management Subsystem Health Event" 
--#SUMMARY    "Management controller Available" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "PXE boot completed"           r--#TYPE       "OS Boot Event" 
--#SUMMARY    "PXE boot completed" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 C"Critical Under-Voltage problem (Lower non-recoverable, going low)"           �--#TYPE       "Voltage Event" 
--#SUMMARY    "Under-Voltage Warning (Lower non-recoverable, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "Diagnostic boot Incomplete"           t--#TYPE       "OS Boot Event" 
--#SUMMARY    "Diagnostic boot Incomplete" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 "Processor Presence Detected"           }--#TYPE       "Processor Event" 
--#SUMMARY    "Processor Presence Detected" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "System Event Logging Disabled"           {--#TYPE       "System Event Log" 
--#SUMMARY    "System Event Logging Disabled" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 !"Hard Disk Drive In Failed Array"           �--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive In Failed Array" 
--#ARGUMENTS    {} 
--#SEVERITY     CRITICAL 
 '"Fan Redundancy is in a degraded state"           {--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Redundancy is in a degraded state" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 )"Power Supply input lost or out-of-range"           �--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply input lost or out-of-range" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 ?"Critical Over-Temperature problem (Upper critical, going low)"           �--#TYPE       "Temperature Event" 
--#SUMMARY    "Over-Temperature Warning (Upper critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 '"Slot / Connector - frees spare device"           �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - frees spare device" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 E"Critical Fan Under Speed problem (Lower non-recoverable, going low)"           �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Under Speed Warning (Lower non-recoverable, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "OS Watchdog Power Cycle"           x--#TYPE       "Watchdog Event" 
--#SUMMARY    "OS Watchdog Power Cycle" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 0"Power Supply Redundancy Has Returned to Normal"           �--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply Redundancy Has Returned to Normal" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 L"Cooling Device Under Speed Warning (Lower non-critical, going high)Cleared"           �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Under Speed Warning (Lower non-critical, going high)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Watchdog Reset"           j--#TYPE       "Watchdog Event" 
--#SUMMARY    "Watchdog Reset" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 0"Critical Interrupt, IO Channel check NMI error"           �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, IO Channel check NMI error" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 ""OS Watchdog Shut Down Deasserted"           �--#TYPE       "Watchdog Event" 
--#SUMMARY    "OS Watchdog Shut Down Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 `"Critical Interrupt, Bus Degraded (bus operating in a degraded performance state) Event Cleared"           �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, Bus Degraded (bus operating in a degraded performance state) Event Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 )"Correctable Machine Check Error Cleared"           �--#TYPE       "Processor Event" 
--#SUMMARY    "Correctable Machine Check Error Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Controller access Available"           �--#TYPE       "Management Subsystem Health Event" 
--#SUMMARY    "Controller access Available" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 +"Generic Discrete Voltage  (Informational)"           �--#TYPE	      "Voltage Event" 
--#SUMMARY    "Generic Discrete Voltage (Informational)" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ,"System ACPI Power State - Legacy OFF state"           �--#TYPE       "System ACPI Power State Event" 
--#SUMMARY    "System ACPI Power State - Legacy OFF state" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Bootable diskette Found"           z--#TYPE       "Boot Error Event" 
--#SUMMARY    "Bootable diskette Found" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 '"Slot / Connector - Interlock asserted"           �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Interlock asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 B"Critical Over-Current problem (Upper non-recoverable, going low)"           �--#TYPE       "Current Event" 
--#SUMMARY    "Over-Current Warning (Upper non-recoverable, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "Power unit 240VA Power Up"           |--#TYPE       "Power unit event" 
--#SUMMARY    "Power unit 240VA Power Up" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 '"Critical Interrupt, Bus Timeout error"           �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, Bus Timeout error" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 *"Power Supply Configuration error Cleared"           �--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply Configuration error Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "Power Supply Failure Cleared"           �--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply Failure Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Diagnostic boot completed"           y--#TYPE       "OS Boot Event" 
--#SUMMARY    "Diagnostic boot completed" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 1"SM BIOS Uncorrectable CPU-complex Error Cleared"           �--#TYPE       "Processor Event" 
--#SUMMARY    "SM BIOS Uncorrectable CPU-complex Error Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "LAN Leash Lost"           �--#TYPE       "Chassis Intrusion Event" 
--#SUMMARY    "LAN Leash Lost Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 +"OS Watchdog pre-timeout Interrupt Cleared"           �--#TYPE       "Watchdog Event" 
--#SUMMARY    "OS Watchdog pre-timeout Interrupt Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Watchdog Power Cycle"           o--#TYPE       "Watchdog Event" 
--#SUMMARY    "Watchdog Power cycle" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 E"Critical Fan Over Speed problem (Upper non-recoverable, going high)"           �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Under Speed Warning (Upper non-recoverable, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 2"Cooling Device redundancy has returned to Normal"           �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device redundancy has returned to Normal" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 5"Processor BIST (Built In Self Test) Failure Cleared"           �--#TYPE       "Processor Event" 
--#SUMMARY    "Processor BIST (Built In Self Test) Failure Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 :"System Boot / Restart Initiated by Hard Reset Deasserted"           �--#TYPE       "System Boot / Restart Event" 
--#SUMMARY    "System Boot / Restart Initiated by Hard Reset Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 2"Hard Disk Drive is present or has been inserted."           �--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive is present or has been inserted." 
--#ARGUMENTS    {} 
--#SEVERITY     INFORMATIONAL 
 ?"Under-Current Warning (Lower non-critical, going high)Cleared"           �--#TYPE       "Current Event" 
--#SUMMARY    "Under-Current Warning (Lower non-critical, going high)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 <"Under-Temperature Warning (Lower non-critical, going high)"           �--#TYPE       "Temperature Event" 
--#SUMMARY    "Under-Temperature Warning (Lower non-critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
  "BIOS Watchdog Reset Deasserted"           --#TYPE       "Watchdog Event" 
--#SUMMARY    "BIOS Watchdog Reset Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 '"Slot / Connector - holds spare device"           �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - holds spare device" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 G"Critical Fan Under Speed problem (Lower critical, going high) Cleared"           �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Under Speed Warning (Lower critical, going high) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 +"OS Stop / Shutdown - Agent Not Responding"           �--#TYPE       "OS Stop / Shutdown Event" 
--#SUMMARY    "OS Stop / Shutdown - Agent Not Responding" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 9"Fan Under Speed Warning (Lower non-critical, going low)"           �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Under Speed Warning (Lower non-critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 %"System Firmware Progress Completed "           �--#TYPE       "System Firmware Progress Event" 
--#SUMMARY    "System Firmware Progress Completed " 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Memory Presence detected."           x--#TYPE       "Memory Event" 
--#SUMMARY    "Memory Presence detected." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "FRU Deactivation Requested"           |--#TYPE       "FRU State Event" 
--#SUMMARY    "FRU Deactivation Requested" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 *"Platform Alert - platform generated page"           �--#TYPE       "Platform Alert Event" 
--#SUMMARY    "Platform Alert- platform generated page" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ."Power Supply input out-of-range, but present"           �--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply input out-of-range, but present" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 ("Power Supply is connected to AC Power."           �--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply is connected to AC Power." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 +"Controller access degraded or unavailable"           �--#TYPE       "Management Subsystem Health Event" 
--#SUMMARY    "Controller access degraded or unavailable" 
--#ARGUMENTS  {} 
--#SEVERITY   MAJOR 
 K"Generic Non-Critical Voltage Problem (Transition to Non-critical from OK)"           �--#TYPE	      "Voltage Event" 
--#SUMMARY    "Generic Critical Voltage Problem (Transition to Non-critical from OK)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 *"Power Supply Predictive Failure Asserted"           �--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply Predictive Failure Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "CDROM boot completed"           t--#TYPE       "OS Boot Event" 
--#SUMMARY    "CDROM boot completed" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Power Supply AC Restored"           }--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply AC Restored" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Fan Inserted/Present"           p--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Inserted/Present" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "OS Watchdog Power Down"           w--#TYPE       "Watchdog Event" 
--#SUMMARY    "OS Watchdog Power Down" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 3"Other Pre-boot Password Violation Attempt Cleared"           �--#TYPE       "Platform Securtiy Violation Attempt Event" 
--#SUMMARY    "Other pre-boot Password Violation Attempt Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
                                             ;"Timestamp of Local Date and Time when alert was generated"                       0"SP System Identification - Text Identification"                       '"Host System UUID(Universal Unique ID)"                       "Host System Serial Number"                       �"Alert Severity Value
                          - Information(0)
                          - Warning(1)
                          - Critical(2)
                          - Recovery(8)"                       "Alert Message Text"                       "Alert Message ID"                       "Alert Message ID"                       "Host Contact"                       "Host Location"                       "Host Location - Room ID"                       "Host Location - Rack ID"                       #"Host Location - Lowest U-position"                       "Host Location - BladeBay"                       "Event Identifier"                       "Serviceability information."                       )"This event generated for test purposes."                       ;"Ordered list of Failing FRU Numbers, separated by commas."                       *"Machine Type and Model for failing host."                       6"Auxiliary data that may be included for some events."                       "Manufacture name"                       "System model"                       "Sensor Name"                       "Sensor Type"                       "Current Sensor Reading"                       ~"Sensor Threshold: LowerNonRecoverable, LowerCritical, LowerNonCritical, UpperNonCritical, UpperCritical, UpperNonRecoverable"                       	"Host OS"                       "Board name."                       "Board Type"                       "Board Status"                       "System Name"                       "Trap Test for v2c, v3"           -- ENTERPRISE petevts 
     ;"Under-Temperature Warning (Lower non-critical, going low)"           -- ENTERPRISE petevts 
   �--#TYPE       "Temperature Event" 
--#SUMMARY    "Under-Temperature Warning (Lower non-critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 <"Under-Temperature Warning (Lower non-critical, going high)"           -- ENTERPRISE petevts 
   �--#TYPE       "Temperature Event" 
--#SUMMARY    "Under-Temperature Warning (Lower non-critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 @"Critical Under-Temperature problem (Lower critical, going low)"           -- ENTERPRISE petevts 
   �--#TYPE       "Temperature Event" 
--#SUMMARY    "Under-Temperature Warning (Lower critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 A"Critical Under-Temperature problem (Lower critical, going high)"           -- ENTERPRISE petevts 
   �--#TYPE       "Temperature Event" 
--#SUMMARY    "Under-Temperature Warning (Lower critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 G"Critical Under-Temperature problem (Lower non-recoverable, going low)"           -- ENTERPRISE petevts 
   �--#TYPE       "Temperature Event" 
--#SUMMARY    "Under-Temperature Warning (Lower non-recoverable, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 H"Critical Under-Temperature problem (Lower non-recoverable, going high)"           -- ENTERPRISE petevts 
   �--#TYPE       "Temperature Event" 
--#SUMMARY    "Under-Temperature Warning (Lower non-recoverable, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 :"Over-Temperature Warning (Upper non-critical, going low)"           -- ENTERPRISE petevts 
   �--#TYPE       "Temperature Event" 
--#SUMMARY    "Over-Temperature Warning (Upper non-critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 ;"Over-Temperature Warning (Upper non-critical, going high)"           -- ENTERPRISE petevts 
   �--#TYPE       "Temperature Event" 
--#SUMMARY    "Over-Temperature Warning (Upper non-critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 ?"Critical Over-Temperature problem (Upper critical, going low)"           -- ENTERPRISE petevts 
   �--#TYPE       "Temperature Event" 
--#SUMMARY    "Over-Temperature Warning (Upper critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 @"Critical Over-Temperature problem (Upper critical, going high)"           -- ENTERPRISE petevts 
   �--#TYPE       "Temperature Event" 
--#SUMMARY    "Over-Temperature Warning (Upper critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 F"Critical Over-Temperature problem (Upper non-recoverable, going low)"           -- ENTERPRISE petevts 
   �--#TYPE       "Temperature Event" 
--#SUMMARY    "Over-Temperature Warning (Upper non-recoverable, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 G"Critical Over-Temperature problem (Upper non-recoverable, going high)"           -- ENTERPRISE petevts 
   �--#TYPE       "Temperature Event" 
--#SUMMARY    "Under-Temperature Warning (Upper non-recoverable, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 C"Under-Temperature Warning (Lower non-critical, going low) Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Temperature Event" 
--#SUMMARY    "Under-Temperature Warning (Lower non-critical, going low) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 C"Under-Temperature Warning (Lower non-critical, going high)Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Temperature Event" 
--#SUMMARY    "Under-Temperature Warning (Lower non-critical, going high)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 G"Critical Under-Temperature problem (Lower critical, going low)Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Temperature Event" 
--#SUMMARY    "Under-Temperature Warning (Lower critical, going low)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 I"Critical Under-Temperature problem (Lower critical, going high) Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Temperature Event" 
--#SUMMARY    "Under-Temperature Warning (Lower critical, going high) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 N"Critical Under-Temperature problem (Lower non-recoverable, going low)Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Temperature Event" 
--#SUMMARY    "Under-Temperature Warning (Lower non-recoverable, going low)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 P"Critical Under-Temperature problem (Lower non-recoverable, going high) Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Temperature Event" 
--#SUMMARY    "Under-Temperature Warning (Lower non-recoverable, going high) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 B"Over-Temperature Warning (Upper non-critical, going low) Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Temperature Event" 
--#SUMMARY    "Over-Temperature Warning (Upper non-critical, going low) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 B"Over-Temperature Warning (Upper non-critical, going high)Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Temperature Event" 
--#SUMMARY    "Over-Temperature Warning (Upper non-critical, going high)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 G"Critical Over-Temperature problem (Upper critical, going low) Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Temperature Event" 
--#SUMMARY    "Over-Temperature Warning (Upper critical, going low) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 G"Critical Over-Temperature problem (Upper critical, going high)Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Temperature Event" 
--#SUMMARY    "Over-Temperature Warning (Upper critical, going high)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 M"Critical Over-Temperature problem (Upper non-recoverable, going low)Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Temperature Event" 
--#SUMMARY    "Over-Temperature Warning (Upper non-recoverable, going low)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 O"Critical Over-Temperature problem (Upper non-recoverable, going high) Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Temperature Event" 
--#SUMMARY    "Under-Temperature Warning (Upper non-recoverable, going high) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 P"Generic Critical Temperature Problem (Transition to Critical from less severe)"           -- ENTERPRISE petevts 
   �--#TYPE       "Temperature Event" 
--#SUMMARY    "Generic Critical Temperature Problem (Transition to Critical from less severe)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 F"Generic Temperature Warning (Transition to Warning from less severe)"           -- ENTERPRISE petevts 
   �--#TYPE	      "Temperature Event" 
--#SUMMARY    "Generic Temperature Warning (Transition to Warning from less severe)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 7"Under-Voltage Warning (Lower non-critical, going low)"           -- ENTERPRISE petevts 
   �--#TYPE       "Voltage Event" 
--#SUMMARY    "Under-Voltage Warning (Lower non-critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 8"Under-Voltage Warning (Lower non-critical, going high)"           -- ENTERPRISE petevts 
   �--#TYPE       "Voltage Event" 
--#SUMMARY    "Under-Voltage Warning (Lower non-critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 <"Critical Under-Voltage problem (Lower critical, going low)"           -- ENTERPRISE petevts 
   �--#TYPE       "Voltage Event" 
--#SUMMARY    "Under-Voltage Warning (Lower critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 ="Critical Under-Voltage problem (Lower critical, going high)"           -- ENTERPRISE petevts 
   �--#TYPE       "Voltage Event" 
--#SUMMARY    "Under-Voltage Warning (Lower critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 C"Critical Under-Voltage problem (Lower non-recoverable, going low)"           -- ENTERPRISE petevts 
   �--#TYPE       "Voltage Event" 
--#SUMMARY    "Under-Voltage Warning (Lower non-recoverable, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 D"Critical Under-Voltage problem (Lower non-recoverable, going high)"           -- ENTERPRISE petevts 
   �--#TYPE       "Voltage Event" 
--#SUMMARY    "Under-Voltage Warning (Lower non-recoverable, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 6"Over-Voltage Warning (Upper non-critical, going low)"           -- ENTERPRISE petevts 
   �--#TYPE       "Voltage Event" 
--#SUMMARY    "Over-Voltage Warning (Upper non-critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 7"Over-Voltage Warning (Upper non-critical, going high)"           -- ENTERPRISE petevts 
   �--#TYPE       "Voltage Event" 
--#SUMMARY    "Over-Voltage Warning (Upper non-critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 ;"Critical Over-Voltage problem (Upper critical, going low)"           -- ENTERPRISE petevts 
   �--#TYPE       "Voltage Event" 
--#SUMMARY    "Over-Voltage Warning (Upper critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 <"Critical Over-Voltage problem (Upper critical, going high)"           -- ENTERPRISE petevts 
   �--#TYPE       "Voltage Event" 
--#SUMMARY    "Over-Voltage Warning (Upper critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 B"Critical Over-Voltage problem (Upper non-recoverable, going low)"           -- ENTERPRISE petevts 
   �--#TYPE       "Voltage Event" 
--#SUMMARY    "Over-Voltage Warning (Upper non-recoverable, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 C"Critical Over-Voltage problem (Upper non-recoverable, going high)"           -- ENTERPRISE petevts 
   �--#TYPE       "Voltage Event" 
--#SUMMARY    "Under-Voltage Warning (Upper non-recoverable, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 ?"Under-Voltage Warning (Lower non-critical, going low) Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Voltage Event" 
--#SUMMARY    "Under-Voltage Warning (Lower non-critical, going low) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ?"Under-Voltage Warning (Lower non-critical, going high)Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Voltage Event" 
--#SUMMARY    "Under-Voltage Warning (Lower non-critical, going high)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 C"Critical Under-Voltage problem (Lower critical, going low)Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Voltage Event" 
--#SUMMARY    "Under-Voltage Warning (Lower critical, going low)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 E"Critical Under-Voltage problem (Lower critical, going high) Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Voltage Event" 
--#SUMMARY    "Under-Voltage Warning (Lower critical, going high) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 J"Critical Under-Voltage problem (Lower non-recoverable, going low)Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Voltage Event" 
--#SUMMARY    "Under-Voltage Warning (Lower non-recoverable, going low)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 L"Critical Under-Voltage problem (Lower non-recoverable, going high) Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Voltage Event" 
--#SUMMARY    "Under-Voltage Warning (Lower non-recoverable, going high) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 >"Over-Voltage Warning (Upper non-critical, going low) Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Voltage Event" 
--#SUMMARY    "Over-Voltage Warning (Upper non-critical, going low) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 >"Over-Voltage Warning (Upper non-critical, going high)Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Voltage Event" 
--#SUMMARY    "Over-Voltage Warning (Upper non-critical, going high)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 C"Critical Over-Voltage problem (Upper critical, going low) Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Voltage Event" 
--#SUMMARY    "Over-Voltage Warning (Upper critical, going low) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 C"Critical Over-Voltage problem (Upper critical, going high)Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Voltage Event" 
--#SUMMARY    "Over-Voltage Warning (Upper critical, going high)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 I"Critical Over-Voltage problem (Upper non-recoverable, going low)Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Voltage Event" 
--#SUMMARY    "Over-Voltage Warning (Upper non-recoverable, going low)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 K"Critical Over-Voltage problem (Upper non-recoverable, going high) Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Voltage Event" 
--#SUMMARY    "Under-Voltage Warning (Upper non-recoverable, going high) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 *"Generic Critical Voltage Problem Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Voltage Event" 
--#SUMMARY    "Generic Critical Voltage Problem Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 L"Generic Critical Voltage Problem (Transition to Critical from less severe)"           -- ENTERPRISE petevts 
   �--#TYPE       "Voltage Event" 
--#SUMMARY    "Generic Critical Voltage Problem (Transition to Critical from less severe)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 <"Generic Critical Voltage Problem Cleared(Transition to OK)"           -- ENTERPRISE petevts 
   �--#TYPE	      "Voltage Event" 
--#SUMMARY    "Generic Critical Voltage Problem Cleared(Transition to OK)" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 K"Generic Non-Critical Voltage Problem (Transition to Non-critical from OK)"           -- ENTERPRISE petevts 
   �--#TYPE	      "Voltage Event" 
--#SUMMARY    "Generic Critical Voltage Problem (Transition to Non-critical from OK)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 L"Generic Critical Voltage Problem (Transition to Critical from less severe)"           -- ENTERPRISE petevts 
   �--#TYPE	      "Voltage Event" 
--#SUMMARY    "Generic Critical Voltage Problem (Transition to Critical from less severe)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 G"Generic Voltage Warning (Transition to Non-Critical from less severe)"           -- ENTERPRISE petevts 
   �--#TYPE	      "Voltage Event" 
--#SUMMARY    "Generic Voltage Warning (Transition to Non-Critical from less severe)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 G"Generic Voltage Warning (Transition to Non-Critical from more severe)"           -- ENTERPRISE petevts 
   �--#TYPE	      "Voltage Event" 
--#SUMMARY    "Generic Voltage Warning (Transition to Non-Critical from more severe)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 9"Generic Voltage Warning (Transition to Non-Recoverable)"           -- ENTERPRISE petevts 
   �--#TYPE	      "Voltage Event" 
--#SUMMARY    "Generic Voltage Warning (Transition to Non-Recoverable)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 %"Generic Discrete Voltage  (Monitor)"           -- ENTERPRISE petevts 
   �--#TYPE	      "Voltage Event" 
--#SUMMARY    "Generic Discrete Voltage (Monitor)" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 +"Generic Discrete Voltage  (Informational)"           -- ENTERPRISE petevts 
   �--#TYPE	      "Voltage Event" 
--#SUMMARY    "Generic Discrete Voltage (Informational)" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 7"Under-Current Warning (Lower non-critical, going low)"           -- ENTERPRISE petevts 
   �--#TYPE       "Current Event" 
--#SUMMARY    "Under-Current Warning (Lower non-critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 8"Under-Current Warning (Lower non-critical, going high)"           -- ENTERPRISE petevts 
   �--#TYPE       "Current Event" 
--#SUMMARY    "Under-Current Warning (Lower non-critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 <"Critical Under-Current problem (Lower critical, going low)"           -- ENTERPRISE petevts 
   �--#TYPE       "Current Event" 
--#SUMMARY    "Under-Current Warning (Lower critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 ="Critical Under-Current problem (Lower critical, going high)"           -- ENTERPRISE petevts 
   �--#TYPE       "Current Event" 
--#SUMMARY    "Under-Current Warning (Lower critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 C"Critical Under-Current problem (Lower non-recoverable, going low)"           -- ENTERPRISE petevts 
   �--#TYPE       "Current Event" 
--#SUMMARY    "Under-Current Warning (Lower non-recoverable, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 D"Critical Under-Current problem (Lower non-recoverable, going high)"           -- ENTERPRISE petevts 
   �--#TYPE       "Current Event" 
--#SUMMARY    "Under-Current Warning (Lower non-recoverable, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 6"Over-Current Warning (Upper non-critical, going low)"           -- ENTERPRISE petevts 
   �--#TYPE       "Current Event" 
--#SUMMARY    "Over-Current Warning (Upper non-critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 7"Over-Current Warning (Upper non-critical, going high)"           -- ENTERPRISE petevts 
   �--#TYPE       "Current Event" 
--#SUMMARY    "Over-Current Warning (Upper non-critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 ;"Critical Over-Current problem (Upper critical, going low)"           -- ENTERPRISE petevts 
   �--#TYPE       "Current Event" 
--#SUMMARY    "Over-Current Warning (Upper critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 <"Critical Over-Current problem (Upper critical, going high)"           -- ENTERPRISE petevts 
   �--#TYPE       "Current Event" 
--#SUMMARY    "Over-Current Warning (Upper critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 B"Critical Over-Current problem (Upper non-recoverable, going low)"           -- ENTERPRISE petevts 
   �--#TYPE       "Current Event" 
--#SUMMARY    "Over-Current Warning (Upper non-recoverable, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 C"Critical Over-Current problem (Upper non-recoverable, going high)"           -- ENTERPRISE petevts 
   �--#TYPE       "Current Event" 
--#SUMMARY    "Under-Current Warning (Upper non-recoverable, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 ?"Under-Current Warning (Lower non-critical, going low) Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Current Event" 
--#SUMMARY    "Under-Current Warning (Lower non-critical, going low) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ?"Under-Current Warning (Lower non-critical, going high)Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Current Event" 
--#SUMMARY    "Under-Current Warning (Lower non-critical, going high)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 C"Critical Under-Current problem (Lower critical, going low)Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Current Event" 
--#SUMMARY    "Under-Current Warning (Lower critical, going low)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 E"Critical Under-Current problem (Lower critical, going high) Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Current Event" 
--#SUMMARY    "Under-Current Warning (Lower critical, going high) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 J"Critical Under-Current problem (Lower non-recoverable, going low)Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Current Event" 
--#SUMMARY    "Under-Current Warning (Lower non-recoverable, going low)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 L"Critical Under-Current problem (Lower non-recoverable, going high) Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Current Event" 
--#SUMMARY    "Under-Current Warning (Lower non-recoverable, going high) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 >"Over-Current Warning (Upper non-critical, going low) Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Current Event" 
--#SUMMARY    "Over-Current Warning (Upper non-critical, going low) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 >"Over-Current Warning (Upper non-critical, going high)Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Current Event" 
--#SUMMARY    "Over-Current Warning (Upper non-critical, going high)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 C"Critical Over-Current problem (Upper critical, going low) Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Current Event" 
--#SUMMARY    "Over-Current Warning (Upper critical, going low) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 C"Critical Over-Current problem (Upper critical, going high)Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Current Event" 
--#SUMMARY    "Over-Current Warning (Upper critical, going high)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 I"Critical Over-Current problem (Upper non-recoverable, going low)Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Current Event" 
--#SUMMARY    "Over-Current Warning (Upper non-recoverable, going low)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 K"Critical Over-Current problem (Upper non-recoverable, going high) Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Current Event" 
--#SUMMARY    "Under-Current Warning (Upper non-recoverable, going high) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 9"Fan Under Speed Warning (Lower non-critical, going low)"           -- ENTERPRISE petevts 
   �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Under Speed Warning (Lower non-critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 :"Fan Under Speed Warning (Lower non-critical, going high)"           -- ENTERPRISE petevts 
   �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Under Speed Warning (Lower non-critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 >"Critical Fan Under Speed problem (Lower critical, going low)"           -- ENTERPRISE petevts 
   �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Under Speed Warning (Lower critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 ?"Critical Fan Under Speed problem (Lower critical, going high)"           -- ENTERPRISE petevts 
   �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Under Speed Warning (Lower critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 E"Critical Fan Under Speed problem (Lower non-recoverable, going low)"           -- ENTERPRISE petevts 
   �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Under Speed Warning (Lower non-recoverable, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 F"Critical Fan Under Speed problem (Lower non-recoverable, going high)"           -- ENTERPRISE petevts 
   �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Under Speed Warning (Lower non-recoverable, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 8"Fan Over Speed Warning (Upper non-critical, going low)"           -- ENTERPRISE petevts 
   �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Over Speed Warning (Upper non-critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 9"Fan Over Speed Warning (Upper non-critical, going high)"           -- ENTERPRISE petevts 
   �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Over Speed Warning (Upper non-critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 ="Critical Fan Over Speed problem (Upper critical, going low)"           -- ENTERPRISE petevts 
   �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Over Speed Warning (Upper critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 >"Critical Fan Over Speed problem (Upper critical, going high)"           -- ENTERPRISE petevts 
   �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Over Speed Warning (Upper critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 D"Critical Fan Over Speed problem (Upper non-recoverable, going low)"           -- ENTERPRISE petevts 
   �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Over Speed Warning (Upper non-recoverable, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 E"Critical Fan Over Speed problem (Upper non-recoverable, going high)"           -- ENTERPRISE petevts 
   �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Under Speed Warning (Upper non-recoverable, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "test"           -- ENTERPRISE petevts 
   �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Under Speed Warning (Upper non-recoverable, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 A"Fan Under Speed Warning (Lower non-critical, going low) Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Under Speed Warning (Lower non-critical, going low) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 A"Fan Under Speed Warning (Lower non-critical, going high)Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Under Speed Warning (Lower non-critical, going high)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 E"Critical Fan Under Speed problem (Lower critical, going low)Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Under Speed Warning (Lower critical, going low)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 G"Critical Fan Under Speed problem (Lower critical, going high) Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Under Speed Warning (Lower critical, going high) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 L"Critical Fan Under Speed problem (Lower non-recoverable, going low)Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Under Speed Warning (Lower non-recoverable, going low)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 N"Critical Fan Under Speed problem (Lower non-recoverable, going high) Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Under Speed Warning (Lower non-recoverable, going high) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 @"Fan Over Speed Warning (Upper non-critical, going low) Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Over Speed Warning (Upper non-critical, going low) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 @"Fan Over Speed Warning (Upper non-critical, going high)Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Over Speed Warning (Upper non-critical, going high)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 E"Critical Fan Over Speed problem (Upper critical, going low) Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Over Speed Warning (Upper critical, going low) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 E"Critical Fan Over Speed problem (Upper critical, going high)Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Over Speed Warning (Upper critical, going high)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 K"Critical Fan Over Speed problem (Upper non-recoverable, going low)Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Over Speed Warning (Upper non-recoverable, going low)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 M"Critical Fan Over Speed problem (Upper non-recoverable, going high) Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Under Speed Warning (Upper non-recoverable, going high) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Fan Removed/Absent"           -- ENTERPRISE petevts 
   i--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Removed/Absent" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "Fan Inserted/Present"           -- ENTERPRISE petevts 
   p--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Inserted/Present" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 '"Fan redundancy has returned to Normal"           -- ENTERPRISE petevts 
   �--#TYPE       "Fan Event" 
--#SUMMARY    "Fan redundancy has returned to Normal" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Fan Redundancy has been Lost"           -- ENTERPRISE petevts 
   s--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Redundancy has been Lost" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 '"Fan Redundancy is in a degraded state"           -- ENTERPRISE petevts 
   {--#TYPE       "Fan Event" 
--#SUMMARY    "Fan Redundancy is in a degraded state" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 1"Chassis Intrusion - Physical Security Violation"           -- ENTERPRISE petevts 
   �--#TYPE       "Chassis Intrusion Event" 
--#SUMMARY    "Chassis Intrusion - Physical Security Violation" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 )"Chassis Intrusion - Drive Bay Violation"           -- ENTERPRISE petevts 
   �--#TYPE       "Chassis Intrusion Event" 
--#SUMMARY    "Chassis Intrusion - Drive Bay Violation" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "I/O Card Area Intrusion"           -- ENTERPRISE petevts 
   |--#TYPE       "Chassis Intrusion Event" 
--#SUMMARY    "I/O Card Area Intrusion" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "Processor Area Intrusion"           -- ENTERPRISE petevts 
   }--#TYPE       "Chassis Intrusion Event" 
--#SUMMARY    "Processor Area Intrusion" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "LAN Leash Lost"           -- ENTERPRISE petevts 
   s--#TYPE       "Chassis Intrusion Event" 
--#SUMMARY    "LAN Leash Lost" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "Unauthorized dock"           -- ENTERPRISE petevts 
   v--#TYPE       "Chassis Intrusion Event" 
--#SUMMARY    "Unauthorized dock" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "Fan Area Intrusion"           -- ENTERPRISE petevts 
   w--#TYPE       "Chassis Intrusion Event" 
--#SUMMARY    "Fan Area Intrusion" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 ?"Chassis Intrusion (Physical Security Violation) Event Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Chassis Intrusion Event" 
--#SUMMARY    "Chassis Intrusion( Physical Security Violation) Event Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 1"Chassis Intrusion - Drive Bay Violation Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Chassis Intrusion Event" 
--#SUMMARY    "Chassis Intrusion - Drive Bay Violation Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 !"I/O Card Area Intrusion Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Chassis Intrusion Event" 
--#SUMMARY    "I/O Card Area Intrusion Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ""Processor Area Intrusion Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Chassis Intrusion Event" 
--#SUMMARY    "Processor Area Intrusion Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "LAN Leash Lost"           -- ENTERPRISE petevts 
   �--#TYPE       "Chassis Intrusion Event" 
--#SUMMARY    "LAN Leash Lost Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Unauthorized dock Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Chassis Intrusion Event" 
--#SUMMARY    "Unauthorized dock Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Fan Area Intrusion Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Chassis Intrusion Event" 
--#SUMMARY    "Fan Area Intrusion Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Secure Mode Violation Attempt"           -- ENTERPRISE petevts 
   �--#TYPE       "Platform Securtiy Violation Attempt Event" 
--#SUMMARY    "Secure Mode Violation Attempt" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 !"User Password Violation Attempt"           -- ENTERPRISE petevts 
   �--#TYPE       "Platform Securtiy Violation Attempt Event" 
--#SUMMARY    "User Password Violation Attempt" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 ""Setup Password Violation Attempt"           -- ENTERPRISE petevts 
   �--#TYPE       "Platform Securtiy Violation Attempt Event" 
--#SUMMARY    "Setup Password Violation Attempt" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 )"Network Boot Password Violation Attempt"           -- ENTERPRISE petevts 
   �--#TYPE       "Platform Securtiy Violation Attempt Event" 
--#SUMMARY    "Network boot Password Violation Attempt" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 +"Other Pre-boot Password Violation Attempt"           -- ENTERPRISE petevts 
   �--#TYPE       "Platform Securtiy Violation Attempt Event" 
--#SUMMARY    "Other pre-boot Password Violation Attempt" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 &"Out-of-band access Violation Attempt"           -- ENTERPRISE petevts 
   �--#TYPE       "Platform Securtiy Violation Attempt Event" 
--#SUMMARY    "Out-of-band access Violation Attempt" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 '"Secure Mode Violation Attempt Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Platform Securtiy Violation Attempt Event" 
--#SUMMARY    "Secure Mode Violation Attempt Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 )"User Password Violation Attempt Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Platform Securtiy Violation Attempt Event" 
--#SUMMARY    "User Password Violation Attempt Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 *"Setup Password Violation Attempt Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Platform Securtiy Violation Attempt Event" 
--#SUMMARY    "Setup Password Violation Attempt Cleared"  
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 1"Network Boot Password Violation Attempt Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Platform Securtiy Violation Attempt Event" 
--#SUMMARY    "Network boot Password Violation Attempt Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 3"Other Pre-boot Password Violation Attempt Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Platform Securtiy Violation Attempt Event" 
--#SUMMARY    "Other pre-boot Password Violation Attempt Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ."Out-of-band access Violation Attempt Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Platform Securtiy Violation Attempt Event" 
--#SUMMARY    "Out-of-band access Violation Attempt Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Processor Internal Error"           -- ENTERPRISE petevts 
   u--#TYPE       "Processor Event" 
--#SUMMARY    "Processor Internal Error" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 4"Processor Thermal Trip (Over Temperature Shutdown)"           -- ENTERPRISE petevts 
   �--#TYPE       "Processor Event" 
--#SUMMARY    "Processor Thermal Trip (Over Temperature Shutdown)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 O"Processor Fault Resilient Booting (FRB) 1 / BIST (Built In Self Test) Failure"           -- ENTERPRISE petevts 
   �--#TYPE       "Processor Event" 
--#SUMMARY    "Processor Fault Resilient Booting (FRB) 1 / Processor BIST (Built In Self Test) Failure" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 W"Processor Fault Resilient Booting (FRB) 2 / Hang in Power On Self Test (POST) Failure"           -- ENTERPRISE petevts 
   �--#TYPE       "Processor Event" 
--#SUMMARY    "Processor Fault Resilient Booting (FRB) 2 / Hang in Power On Self Test (POST) Failure" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL  
 V"Processor Fault Resilient Booting (FRB) 3 / Processor Setup / Initialization Failure"           -- ENTERPRISE petevts 
   �--#TYPE	"Processor Event" 
--#SUMMARY    "Processor Fault Resilient Booting (FRB) 3 / Processor Setup / Initialization Failure" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "Processor Configuration Error"           -- ENTERPRISE petevts 
   z--#TYPE       "Processor Event" 
--#SUMMARY    "Processor Configuration Error" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 )"SM BIOS Uncorrectable CPU-complex Error"           -- ENTERPRISE petevts 
   �--#TYPE       "Processor Event" 
--#SUMMARY    "SM BIOS Uncorrectable CPU-complex Error" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "Processor Presence Detected"           -- ENTERPRISE petevts 
   }--#TYPE       "Processor Event" 
--#SUMMARY    "Processor Presence Detected" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Processor Disabled"           -- ENTERPRISE petevts 
   t--#TYPE       "Processor Event" 
--#SUMMARY    "Processor Disabled" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Terminator Presence Detected"           -- ENTERPRISE petevts 
   ~--#TYPE       "Processor Event" 
--#SUMMARY    "Terminator Presence Detected" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 /"Processor Throttled (Processor Speed Reduced)"           -- ENTERPRISE petevts 
   �--#TYPE       "Processor Event" 
--#SUMMARY    "Processor Throttled (Processor Speed Reduced)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 ""Processor Internal Error Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Processor Event" 
--#SUMMARY    "Processor Internal Error Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 <"Processor Thermal Trip (Over Temperature Shutdown) Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Processor Event" 
--#SUMMARY    "Processor Thermal Trip (Over Temperature Shutdown) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 5"Processor BIST (Built In Self Test) Failure Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Processor Event" 
--#SUMMARY    "Processor BIST (Built In Self Test) Failure Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 _"Processor Fault Resilient Booting (FRB) 2 / Hang in Power On Self Test (POST) Failure Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Processor Event" 
--#SUMMARY    "Processor Fault Resilient Booting (FRB) 2 / Hang in Power On Self Test (POST) Failure Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL  
 ^"Processor Fault Resilient Booting (FRB) 3 / Processor Setup / Initialization Failure Cleared"           -- ENTERPRISE petevts 
   �--#TYPE	"Processor Event" 
--#SUMMARY    "Processor Fault Resilient Booting (FRB) 3 / Processor Setup / Initialization Failure Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 '"Processor Configuration Error Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Processor Event" 
--#SUMMARY    "Processor Configuration Error Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 1"SM BIOS Uncorrectable CPU-complex Error Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Processor Event" 
--#SUMMARY    "SM BIOS Uncorrectable CPU-complex Error Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 5"Processor Throttle Cleared (Normal Processor Speed)"           -- ENTERPRISE petevts 
   �--#TYPE       "Processor Event" 
--#SUMMARY    "Processor Throttle Cleared (Normal Processor Speed)" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 )"Correctable Machine Check Error Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Processor Event" 
--#SUMMARY    "Correctable Machine Check Error Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 -"Power Supply is disconnected from AC Power."           -- ENTERPRISE petevts 
   �--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply is disconnected from AC Power." 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 ("Power Supply is connected to AC Power."           -- ENTERPRISE petevts 
   �--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply is connected to AC Power." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ,"Power Supply Predictive Failure Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply Predictive Failure Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 *"Power Supply Predictive Failure Asserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply Predictive Failure Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 0"Power Supply Redundancy Has Returned to Normal"           -- ENTERPRISE petevts 
   �--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply Redundancy Has Returned to Normal" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 '"Power Supply Redundancy has been Lost"           -- ENTERPRISE petevts 
   �--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply Redundancy has been Lost" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 0"Power Supply Redundancy is in a degraded state"           -- ENTERPRISE petevts 
   �--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply Redundancy is in a degraded state" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 "Power Supply Inserted"           -- ENTERPRISE petevts 
   z--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply Inserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Power supply Failure detected"           -- ENTERPRISE petevts 
   }--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply failure detected" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "Power supply Warning"           -- ENTERPRISE petevts 
   s--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply Warning" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 "Power Supply AC Lost"           -- ENTERPRISE petevts 
   t--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply AC Lost" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 )"Power Supply input lost or out-of-range"           -- ENTERPRISE petevts 
   �--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply input lost or out-of-range" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 ."Power Supply input out-of-range, but present"           -- ENTERPRISE petevts 
   �--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply input out-of-range, but present" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 ""Power Supply Configuration error"           -- ENTERPRISE petevts 
   �--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply Configuration error" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "Power Supply Removed"           -- ENTERPRISE petevts 
   s--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply Removed" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 "Power Supply Failure Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply Failure Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Power Supply Warning Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply Warning Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Power Supply AC Restored"           -- ENTERPRISE petevts 
   }--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply AC Restored" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 2"Power Supply input lost or out-of-range Restored"           -- ENTERPRISE petevts 
   �--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply input lost or out-of-range Restored" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 *"Power Supply input out-of-range restored"           -- ENTERPRISE petevts 
   �--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply input out-of-range restored" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 *"Power Supply Configuration error Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Power Supply Event" 
--#SUMMARY    "Power Supply Configuration error Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 �"Run-time power fault has occurred. This state indicates 
  that one or more DC-DC converter have failed or are not operating 
  within nominal specifications."           -- ENTERPRISE petevts 
   �--#TYPE         "Power Unit Event" 
--#SUMMARY      "Run-time power fault has occurred." 
--#ARGUMENTS    {} 
--#SEVERITY     CRITICAL 
 8"Host power-on sequence has been completed successfully"           -- ENTERPRISE petevts 
   �--#TYPE         "Power Unit Event" 
--#SUMMARY      "Host power-on sequence has been completed successfully." 
--#ARGUMENTS    {} 
--#SEVERITY     INFORMATIONAL 
 )"Power Unit Redundancy has been restored"           -- ENTERPRISE petevts 
   �--#TYPE       "Power Unit Event" 
--#SUMMARY    "Power Unit Redundancy has been restored" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 %"Power Unit Redundancy has been Lost"           -- ENTERPRISE petevts 
   �--#TYPE       "Power Unit Event" 
--#SUMMARY    "Power Unit Redundancy has been Lost" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "Power unit is off."           -- ENTERPRISE petevts 
   u--#TYPE       "Power unit event" 
--#SUMMARY    "Power unit is off." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Power unit is power cycled"           -- ENTERPRISE petevts 
   }--#TYPE       "Power unit event" 
--#SUMMARY    "Power unit is power cycled" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Power unit 240VA Power Down"           -- ENTERPRISE petevts 
   ~--#TYPE       "Power unit event" 
--#SUMMARY    "Power unit 240VA Power Down" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 !"Power unit Interlock Power Down"           -- ENTERPRISE petevts 
   �--#TYPE       "Power unit event" 
--#SUMMARY    "Power unit Interlock Power Down" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 '"Power unit AC lost / Power input lost"           -- ENTERPRISE petevts 
   �--#TYPE       "Power unit event" 
--#SUMMARY    "Power unit AC lost / Power input lost" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Soft Power Control Failure"           -- ENTERPRISE petevts 
   }--#TYPE       "Power unit event" 
--#SUMMARY    "Soft Power Control Failure" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Power Unit Failure detected"           -- ENTERPRISE petevts 
   ~--#TYPE       "Power unit event" 
--#SUMMARY    "Power Unit Failure detected" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Power Unit Predictive Failure"           -- ENTERPRISE petevts 
   �--#TYPE       "Power unit event" 
--#SUMMARY    "Power Unit Predictive Failure" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Power Unit is on."           -- ENTERPRISE petevts 
   t--#TYPE       "Power Unit event" 
--#SUMMARY    "Power Unit is on." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 $"Power unit - Power Cycle Completed"           -- ENTERPRISE petevts 
   �--#TYPE       "Power unit event" 
--#SUMMARY    "Power unit - Power Cycle Completed" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Power unit 240VA Power Up"           -- ENTERPRISE petevts 
   |--#TYPE       "Power unit event" 
--#SUMMARY    "Power unit 240VA Power Up" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Power unit Interlock Power Up"           -- ENTERPRISE petevts 
   �--#TYPE       "Power unit event" 
--#SUMMARY    "Power unit Interlock Power Up" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 $"Power unit AC/Power input restored"           -- ENTERPRISE petevts 
   �--#TYPE       "Power unit event" 
--#SUMMARY    "Power unit AC/Power input restored" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 $"Soft Power Control Failure Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Power unit event" 
--#SUMMARY    "Soft Power Control Failure Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Power Unit Failure Cleared"           -- ENTERPRISE petevts 
   }--#TYPE       "Power unit event" 
--#SUMMARY    "Power Unit Failure Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 '"Power Unit Predictive Failure Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Power unit event" 
--#SUMMARY    "Power Unit Predictive Failure Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 D"Cooling Device Under Speed Warning (Lower non-critical, going low)"           -- ENTERPRISE petevts 
   �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Under Speed Warning (Lower non-critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 E"Cooling Device Under Speed Warning (Lower non-critical, going high)"           -- ENTERPRISE petevts 
   �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Under Speed Warning (Lower non-critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 I"Critical Cooling Device Under Speed problem (Lower critical, going low)"           -- ENTERPRISE petevts 
   �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Under Speed Warning (Lower critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 J"Critical Cooling Device Under Speed problem (Lower critical, going high)"           -- ENTERPRISE petevts 
   �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Under Speed Warning (Lower critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 P"Critical Cooling Device Under Speed problem (Lower non-recoverable, going low)"           -- ENTERPRISE petevts 
   �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Under Speed Warning (Lower non-recoverable, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 Q"Critical Cooling Device Under Speed problem (Lower non-recoverable, going high)"           -- ENTERPRISE petevts 
   �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Under Speed Warning (Lower non-recoverable, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 C"Cooling Device Over Speed Warning (Upper non-critical, going low)"           -- ENTERPRISE petevts 
   �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Over Speed Warning (Upper non-critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 D"Cooling Device Over Speed Warning (Upper non-critical, going high)"           -- ENTERPRISE petevts 
   �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Over Speed Warning (Upper non-critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 H"Critical Cooling Device Over Speed problem (Upper critical, going low)"           -- ENTERPRISE petevts 
   �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Over Speed Warning (Upper critical, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 I"Critical Cooling Device Over Speed problem (Upper critical, going high)"           -- ENTERPRISE petevts 
   �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Over Speed Warning (Upper critical, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 O"Critical Cooling Device Over Speed problem (Upper non-recoverable, going low)"           -- ENTERPRISE petevts 
   �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Over Speed Warning (Upper non-recoverable, going low)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 P"Critical Cooling Device Over Speed problem (Upper non-recoverable, going high)"           -- ENTERPRISE petevts 
   �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Under Speed Warning (Upper non-recoverable, going high)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 L"Cooling Device Under Speed Warning (Lower non-critical, going low) Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Under Speed Warning (Lower non-critical, going low) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 L"Cooling Device Under Speed Warning (Lower non-critical, going high)Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Under Speed Warning (Lower non-critical, going high)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 P"Critical Cooling Device Under Speed problem (Lower critical, going low)Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Under Speed Warning (Lower critical, going low)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 R"Critical Cooling Device Under Speed problem (Lower critical, going high) Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Under Speed Warning (Lower critical, going high) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 W"Critical Cooling Device Under Speed problem (Lower non-recoverable, going low)Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Under Speed Warning (Lower non-recoverable, going low)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 Y"Critical Cooling Device Under Speed problem (Lower non-recoverable, going high) Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Under Speed Warning (Lower non-recoverable, going high) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 K"Cooling Device Over Speed Warning (Upper non-critical, going low) Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Over Speed Warning (Upper non-critical, going low) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 K"Cooling Device Over Speed Warning (Upper non-critical, going high)Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Over Speed Warning (Upper non-critical, going high)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 P"Critical Cooling Device Over Speed problem (Upper critical, going low) Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Over Speed Warning (Upper critical, going low) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 P"Critical Cooling Device Over Speed problem (Upper critical, going high)Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Over Speed Warning (Upper critical, going high)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 V"Critical Cooling Device Over Speed problem (Upper non-recoverable, going low)Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Over Speed Warning (Upper non-recoverable, going low)Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 X"Critical Cooling Device Over Speed problem (Upper non-recoverable, going high) Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Under Speed Warning (Upper non-recoverable, going high) Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Cooling Device Removed/Absent"           -- ENTERPRISE petevts 
   --#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Removed/Absent" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 !"Cooling Device Inserted/Present"           -- ENTERPRISE petevts 
   �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Inserted/Present" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 2"Cooling Device redundancy has returned to Normal"           -- ENTERPRISE petevts 
   �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device redundancy has returned to Normal" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 )"Cooling Device Redundancy has been Lost"           -- ENTERPRISE petevts 
   �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Redundancy has been Lost" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 2"Cooling Device Redundancy is in a degraded state"           -- ENTERPRISE petevts 
   �--#TYPE       "Cooling Device Event" 
--#SUMMARY    "Cooling Device Redundancy is in a degraded state" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 2"Memory Predictive Failure state has been cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Memory Event" 
--#SUMMARY    "Memory Predictive Failure state has been cleared." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 3"Memory Predictive Failure state has been asserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Memory Event" 
--#SUMMARY    "Memory Predictive Failure has been asserted." 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 ="Correctable ECC or other correctable memory error detected."           -- ENTERPRISE petevts 
   �--#TYPE       "Memory Event" 
--#SUMMARY    "Correctable ECC or other correctable memory error detected." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 A"Uncorrectable ECC or other uncorrectable memory error detected."           -- ENTERPRISE petevts 
   �--#TYPE       "Memory Event" 
--#SUMMARY    "Uncorrectable ECC or other uncorrectable memory error detected." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Parity error detected."           -- ENTERPRISE petevts 
   u--#TYPE       "Memory Event" 
--#SUMMARY    "Parity error detected." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Memory Scrub Failed"           -- ENTERPRISE petevts 
   r--#TYPE       "Memory Event" 
--#SUMMARY    "Memory Scrub Failed" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Memory Device Disabled."           -- ENTERPRISE petevts 
   v--#TYPE       "Memory Event" 
--#SUMMARY    "Memory Device Disabled." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 H"Correctable ECC / other correctable memory error logging limit reached"           -- ENTERPRISE petevts 
   �--#TYPE       "Memory Event" 
--#SUMMARY    "Correctable ECC / other correctable memory error logging limit reached" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Memory Presence detected."           -- ENTERPRISE petevts 
   x--#TYPE       "Memory Event" 
--#SUMMARY    "Memory Presence detected." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 &"Memory Configuration Error detected."           -- ENTERPRISE petevts 
   �--#TYPE       "Memory Event" 
--#SUMMARY    "Memory Configuration Error  detected." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Spare Unit of Memory detected"           -- ENTERPRISE petevts 
   |--#TYPE       "Memory Event" 
--#SUMMARY    "Spare Unit of Memory detected" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
  "Memory Automatically Throttled"           -- ENTERPRISE petevts 
   }--#TYPE       "Memory Event" 
--#SUMMARY    "Memory Automatically Throttled" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 )"Memory event - Critical Overtemperature"           -- ENTERPRISE petevts 
   �--#TYPE       "Memory Event" 
--#SUMMARY    "Memory event - Critical Overtemperature" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 <"Correctable ECC or other correctable memory error cleared."           -- ENTERPRISE petevts 
   �--#TYPE       "Memory Event" 
--#SUMMARY    "Correctable ECC or other correctable memory error cleared." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 @"Uncorrectable ECC or other uncorrectable memory error Cleared."           -- ENTERPRISE petevts 
   �--#TYPE       "Memory Event" 
--#SUMMARY    "Uncorrectable ECC or other uncorrectable memory error Cleared." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Parity error Cleared."           -- ENTERPRISE petevts 
   t--#TYPE       "Memory Event" 
--#SUMMARY    "Parity error Cleared." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Memory Scrub Failure Cleared"           -- ENTERPRISE petevts 
   {--#TYPE       "Memory Event" 
--#SUMMARY    "Memory Scrub Failure Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Memory Device Enabled."           -- ENTERPRISE petevts 
   u--#TYPE       "Memory Event" 
--#SUMMARY    "Memory Device Enabled." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 P"Correctable ECC / other correctable memory error logging limit reached Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Memory Event" 
--#SUMMARY    "Correctable ECC / other correctable memory error logging limit reached Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Memory Presence Not detected"           -- ENTERPRISE petevts 
   {--#TYPE       "Memory Event" 
--#SUMMARY    "Memory Presence not detected" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 %"Memory Configuration Error Cleared."           -- ENTERPRISE petevts 
   �--#TYPE       "Memory Event" 
--#SUMMARY    "Memory Configuration Error  Cleared." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ("Spare Unit of Memory detected Deassert"           -- ENTERPRISE petevts 
   �--#TYPE       "Memory Event" 
--#SUMMARY    "Spare Unit of Memory detected Deassert" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ("Memory Automatically Throttled Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Memory Event" 
--#SUMMARY    "Memory Automatically Throttled Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 1"Memory event - Critical Overtemperature Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Memory Event" 
--#SUMMARY    "Memory event - Critical Overtemperature Cleared"s 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 K"This state indicates that a HDD Fault LED which was ON before is OFF now."           -- ENTERPRISE petevts 
   �--#TYPE       "Drive Slot Event" 
--#SUMMARY    "Hard Disk Drive Fault LED is OFF." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "A HDD Fault LED is ON."           -- ENTERPRISE petevts 
   {--#TYPE       "Drive Slot Event" 
--#SUMMARY    "Hard Disk Drive Fault LED is ON." 
--#ARGUMENTS  {} 
--#SEVERITY   MAJOR 
 0"Hard Disk Drive is absent or has been removed."           -- ENTERPRISE petevts 
   �--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive is absent or has been removed." 
--#ARGUMENTS    {} 
--#SEVERITY     INFORMATIONAL 
 "Hard Disk Drive Fault"           -- ENTERPRISE petevts 
   {--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive Fault" 
--#ARGUMENTS    {} 
--#SEVERITY     CRITICAL 
 $"Hard Disk Drive Predictive Failure"           -- ENTERPRISE petevts 
   �--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive Predictive Failure" 
--#ARGUMENTS    {} 
--#SEVERITY     INFORMATIONAL 
 8" Hard Disk Drive Hot Spare (Ready to remove) Asserted "           -- ENTERPRISE petevts 
   �--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive Hot spare (Ready to Remove) " 
--#ARGUMENTS    {} 
--#SEVERITY     INFORMATIONAL 
 >"Hard Disk Drive Consistency Check / Parity Check in progress"           -- ENTERPRISE petevts 
   �--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive Consistency Check / Parity Check in progress" 
--#ARGUMENTS    {} 
--#SEVERITY     INFORMATIONAL 
 #"Hard Disk Drive In Critical Array"           -- ENTERPRISE petevts 
   �--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive In Critical Array" 
--#ARGUMENTS    {} 
--#SEVERITY     INFORMATIONAL 
 !"Hard Disk Drive In Failed Array"           -- ENTERPRISE petevts 
   �--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive In Failed Array" 
--#ARGUMENTS    {} 
--#SEVERITY     CRITICAL 
 +"Hard Disk Drive Rebuild/Remap in progress"           -- ENTERPRISE petevts 
   �--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive Rebuild/Remap in progress" 
--#ARGUMENTS    {} 
--#SEVERITY     INFORMATIONAL 
 '"Hard Disk Drive Rebuild/Remap Aborted"           -- ENTERPRISE petevts 
   �--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive Rebuild/Remap Aborted" 
--#ARGUMENTS    {} 
--#SEVERITY     INFORMATIONAL 
 2"Hard Disk Drive is present or has been inserted."           -- ENTERPRISE petevts 
   �--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive is present or has been inserted." 
--#ARGUMENTS    {} 
--#SEVERITY     INFORMATIONAL 
 "Hard Disk Drive Fault Cleared"           -- ENTERPRISE petevts 
   �--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive Fault Cleared" 
--#ARGUMENTS    {} 
--#SEVERITY     INFORMATIONAL 
 ,"Hard Disk Drive Predictive Failure Cleared"           -- ENTERPRISE petevts 
   �--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive Predictive Failure Cleared" 
--#ARGUMENTS    {} 
--#SEVERITY     INFORMATIONAL 
 &"Hard Disk Drive Hot Spare Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive Hot spare" 
--#ARGUMENTS    {} 
--#SEVERITY     INFORMATIONAL 
 I"Hard Disk Drive Consistency Check / Parity Check in progress Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive Consistency Check / Parity Check in progress Deasserted" 
--#ARGUMENTS    {} 
--#SEVERITY     INFORMATIONAL 
 ."Hard Disk Drive In Critical Array Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive In Critical Array Deasserted" 
--#ARGUMENTS    {} 
--#SEVERITY     INFORMATIONAL 
 ,"Hard Disk Drive In Failed Array Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive In Failed Array Deasserted" 
--#ARGUMENTS    {} 
--#SEVERITY     CRITICAL 
 A"Hard Disk Drive Rebuild/Remap in progress Deasserted(completed)"           -- ENTERPRISE petevts 
   �--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive Rebuild/Remap in progress Deasserted(completed)" 
--#ARGUMENTS    {} 
--#SEVERITY     INFORMATIONAL 
 2"Hard Disk Drive Rebuild/Remap Aborted Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE         "Drive Slot Event" 
--#SUMMARY      "Hard Disk Drive Rebuild/Remap Aborted Deasserted(completed)" 
--#ARGUMENTS    {} 
--#SEVERITY     INFORMATIONAL 
 '"POST Memory Resize Failure Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE       "POST Memory Resize Event" 
--#SUMMARY    "POST Memory Resize Failure Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 %"POST Memory Resize Failure Asserted"           -- ENTERPRISE petevts 
   �--#TYPE       "POST Memory Resize Event" 
--#SUMMARY    "POST Memory Resize Failure Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   MAJOR 
 0"System Firmware Progress: BIOS POST code error"           -- ENTERPRISE petevts 
   �--#TYPE       "System Firmware Progress Event" 
--#SUMMARY    "System Firmware Progress: BIOS POST code error" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "System Firmware Hang"           -- ENTERPRISE petevts 
   �--#TYPE       "System Firmware Progress Event" 
--#SUMMARY    "System Firmware Hang" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "System Firmware Progress"           -- ENTERPRISE petevts 
   �--#TYPE       "System Firmware Progress Event" 
--#SUMMARY    "System Firmware Progress" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 8"System Firmware Progress: BIOS POST code error Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "System Firmware Progress Event" 
--#SUMMARY    "System Firmware Progress: BIOS POST code error Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "System Firmware Hang Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "System Firmware Progress Event" 
--#SUMMARY    "System Firmware Hang Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 %"System Firmware Progress Completed "           -- ENTERPRISE petevts 
   �--#TYPE       "System Firmware Progress Event" 
--#SUMMARY    "System Firmware Progress Completed " 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 +"Correctable Memory Error Logging Disabled"           -- ENTERPRISE petevts 
   �--#TYPE       "System Event Log" 
--#SUMMARY    "Correctable Memory Error Logging Disabled" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Event Type Logging Disabled"           -- ENTERPRISE petevts 
   --#TYPE       "System Event Log" 
--#SUMMARY    "Event Type Logging Disabled." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "SEL Area Reset/Cleared"           -- ENTERPRISE petevts 
   y--#TYPE       "System Event Log" 
--#SUMMARY    "SEL Area Reset/Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "System Event Logging Disabled"           -- ENTERPRISE petevts 
   {--#TYPE       "System Event Log" 
--#SUMMARY    "System Event Logging Disabled" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "SEL Full."           -- ENTERPRISE petevts 
   l--#TYPE       "System Event Log" 
--#SUMMARY    "SEL Full." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "SEL Almost Full."           -- ENTERPRISE petevts 
   s--#TYPE       "System Event Log" 
--#SUMMARY    "SEL Almost Full." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 2"Correctable Machine Check Error Logging Disabled"           -- ENTERPRISE petevts 
   �--#TYPE       "System Event Log" 
--#SUMMARY    "Correctable Machine Check Error Logging Disabled" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 *"Correctable Memory Error Logging Enabled"           -- ENTERPRISE petevts 
   �--#TYPE       "System Event Log" 
--#SUMMARY    "Correctable Memory Error Logging Enabled" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Event Type Logging Enabled"           -- ENTERPRISE petevts 
   ~--#TYPE       "System Event Log" 
--#SUMMARY    "Event Type Logging Enabled." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "SEL Area Reset/Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "System Event Log" 
--#SUMMARY    "SEL Area Reset/Cleared Event Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "System Event Logging Enabled"           -- ENTERPRISE petevts 
   --#TYPE       "System Event Log" 
--#SUMMARY    "System Event Logging Enabled" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "SEL Full Event Cleared"           -- ENTERPRISE petevts 
   y--#TYPE       "System Event Log" 
--#SUMMARY    "SEL Full Event Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "SEL Almost Full Event Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "System Event Log" 
--#SUMMARY    "SEL Almost Full Event Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 1"Correctable Machine Check Error Logging Enabled"           -- ENTERPRISE petevts 
   �--#TYPE       "System Event Log" 
--#SUMMARY    "Correctable Machine Check Error Logging Enabled" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "BIOS Watchdog Reset"           -- ENTERPRISE petevts 
   t--#TYPE       "Watchdog Event" 
--#SUMMARY    "BIOS Watchdog Reset" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "OS Watchdog Reset"           -- ENTERPRISE petevts 
   r--#TYPE       "Watchdog Event" 
--#SUMMARY    "OS Watchdog Reset" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "OS Watchdog Shut Down"           -- ENTERPRISE petevts 
   v--#TYPE       "Watchdog Event" 
--#SUMMARY    "OS Watchdog Shut Down" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "OS Watchdog Power Down"           -- ENTERPRISE petevts 
   w--#TYPE       "Watchdog Event" 
--#SUMMARY    "OS Watchdog Power Down" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "OS Watchdog Power Cycle"           -- ENTERPRISE petevts 
   x--#TYPE       "Watchdog Event" 
--#SUMMARY    "OS Watchdog Power Cycle" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ("OS Watchdog NMI / Diagnostic Interrupt"           -- ENTERPRISE petevts 
   �--#TYPE       "Watchdog Event" 
--#SUMMARY    "OS Watchdog NMI / Diagnostic Interrupt" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ""OS Watchdog Expired, status only"           -- ENTERPRISE petevts 
   �--#TYPE       "Watchdog Event" 
--#SUMMARY    "OS Watchdog Expired, status only" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ,"OS Watchdog pre-timeout Interrupt, non-NMI"           -- ENTERPRISE petevts 
   �--#TYPE       "Watchdog Event" 
--#SUMMARY    "OS Watchdog pre-timeout Interrupt, non-NMI" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
  "BIOS Watchdog Reset Deasserted"           -- ENTERPRISE petevts 
   --#TYPE       "Watchdog Event" 
--#SUMMARY    "BIOS Watchdog Reset Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "OS Watchdog Reset Deasserted"           -- ENTERPRISE petevts 
   }--#TYPE       "Watchdog Event" 
--#SUMMARY    "OS Watchdog Reset Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ""OS Watchdog Shut Down Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Watchdog Event" 
--#SUMMARY    "OS Watchdog Shut Down Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 #"OS Watchdog Power Down Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Watchdog Event" 
--#SUMMARY    "OS Watchdog Power Down Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 $"OS Watchdog Power Cycle Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Watchdog Event" 
--#SUMMARY    "OS Watchdog Power Cycle Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 0"OS Watchdog NMI / Diagnostic Interrupt Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Watchdog Event" 
--#SUMMARY    "OS Watchdog NMI / Diagnostic Interrupt Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 0"OS Watchdog Expired, status only Event Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Watchdog Event" 
--#SUMMARY    "OS Watchdog Expired, status only Event Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 +"OS Watchdog pre-timeout Interrupt Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Watchdog Event" 
--#SUMMARY    "OS Watchdog pre-timeout Interrupt Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "System Reconfigured"           -- ENTERPRISE petevts 
   r--#TYPE       "System Event" 
--#SUMMARY    "System Reconfigured" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "OEM System Boot Event"           -- ENTERPRISE petevts 
   n--#TYPE       "System Event" 
--#SUMMARY    "OEM System Boot Event" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 &"Undetermined system hardware failure"           -- ENTERPRISE petevts 
   ~--#TYPE       "System Event" 
--#SUMMARY    "Undetermined system hardware failure" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 ""SEL Entry added to Auxiliary Log"           -- ENTERPRISE petevts 
   --#TYPE       "System Event" 
--#SUMMARY    "SEL Entry added to Auxiliary Log" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 C"PEF Action is about to be taken. Event filters have been matched."           -- ENTERPRISE petevts 
   �--#TYPE       "System Event" 
--#SUMMARY    "PEF Action is about to be taken. Event filters have been matched." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Timestamp Clock Synch"           -- ENTERPRISE petevts 
   t--#TYPE       "System Event" 
--#SUMMARY    "Timestamp Clock Synch" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 #"System Reconfigured Event Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "System Event" 
--#SUMMARY    "System Reconfigured Event Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "OEM System Boot Event Cleared"           -- ENTERPRISE petevts 
   |--#TYPE       "System Event" 
--#SUMMARY    "OEM System Boot Event Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ."Undetermined system hardware failure Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "System Event" 
--#SUMMARY    "Undetermined system hardware failure Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 -"SEL Entry added to Auxiliary Log Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE       "System Event" 
--#SUMMARY    "SEL Entry added to Auxiliary Log Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "PEF Action Event Deasserted"           -- ENTERPRISE petevts 
   z--#TYPE       "System Event" 
--#SUMMARY    "PEF Action Event Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ("Timestamp Clock Synch Event Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE       "System Event" 
--#SUMMARY    "Timestamp Clock Synch Event Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ("Front Panel NMI / Diagnostic Interrupt"           -- ENTERPRISE petevts 
   �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Front Panel NMI / Diagnostic Interrupt" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 '"Critical Interrupt, Bus Timeout error"           -- ENTERPRISE petevts 
   �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, Bus Timeout error" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 0"Critical Interrupt, IO Channel check NMI error"           -- ENTERPRISE petevts 
   �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, IO Channel check NMI error" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 ("Critical Interrupt, software NMI error"           -- ENTERPRISE petevts 
   �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, software NMI error" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 +"Critical Interrupt, PCI PERR parity error"           -- ENTERPRISE petevts 
   �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, PCI PERR parity error" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 +"Critical Interrupt, PCI SERR parity error"           -- ENTERPRISE petevts 
   �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, PCI SERR parity error" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 ,"Critical Interrupt, EISA Fail Safe Timeout"           -- ENTERPRISE petevts 
   �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, EISA Fail Safe Timeout" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 +"Critical Interrupt, Bus Correctable Error"           -- ENTERPRISE petevts 
   �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, Bus Correctable Error" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 -"Critical Interrupt, Bus Uncorrectable error"           -- ENTERPRISE petevts 
   �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, Bus Uncorrectable error" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 %"Critical Interrupt, Fatal NMI error"           -- ENTERPRISE petevts 
   �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, Fatal NMI error" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 %"Critical Interrupt, Bus Fatal Error"           -- ENTERPRISE petevts 
   �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, Bus Fatal Error" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 R"Critical Interrupt, Bus Degraded (bus operating in a degraded performance state)"           -- ENTERPRISE petevts 
   �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, Bus Degraded (bus operating in a degraded performance state)" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 0"Front Panel NMI / Diagnostic Interrupt Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Front Panel NMI / Diagnostic Interrupt Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 /"Critical Interrupt, Bus Timeout error Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, Bus Timeout error Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 8"Critical Interrupt, IO Channel check NMI error Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, IO Channel check NMI error Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 0"Critical Interrupt, software NMI error Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, software NMI error Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 3"Critical Interrupt, PCI PERR parity error Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, PCI PERR parity error Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 3"Critical Interrupt, PCI SERR parity error Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, PCI SERR parity error Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 :"Critical Interrupt, EISA Fail Safe Timeout Event Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, EISA Fail Safe Timeout Event Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 3"Critical Interrupt, Bus Correctable Error Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, Bus Correctable Error Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 5"Critical Interrupt, Bus Uncorrectable error Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, Bus Uncorrectable error Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 -"Critical Interrupt, Fatal NMI error Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, Fatal NMI error Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 -"Critical Interrupt, Bus Fatal Error Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, Bus Fatal Error Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 `"Critical Interrupt, Bus Degraded (bus operating in a degraded performance state) Event Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Critical Interrupts Event" 
--#SUMMARY    "Critical Interrupt, Bus Degraded (bus operating in a degraded performance state) Event Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Power Button pressed."           -- ENTERPRISE petevts 
   {--#TYPE       "Button/Switch Event" 
--#SUMMARY    "Power Button pressed." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Sleep Button pressed."           -- ENTERPRISE petevts 
   {--#TYPE       "Button/Switch Event" 
--#SUMMARY    "Sleep Button pressed." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Reset Button pressed."           -- ENTERPRISE petevts 
   {--#TYPE       "Button/Switch Event" 
--#SUMMARY    "Reset Button pressed." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 i"FRU latch open (Switch indicating FRU latch is in unlatched position and FRU is mechanically removable)"           -- ENTERPRISE petevts 
   t--#TYPE       "Button/Switch Event" 
--#SUMMARY    "FRU latch open" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "FRU service request button"           -- ENTERPRISE petevts 
   �--#TYPE       "Button/Switch Event" 
--#SUMMARY    "FRU service request button" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Power Button Released."           -- ENTERPRISE petevts 
   |--#TYPE       "Button/Switch Event" 
--#SUMMARY    "Power Button Released." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Sleep Button Released."           -- ENTERPRISE petevts 
   |--#TYPE       "Button/Switch Event" 
--#SUMMARY    "Sleep Button Released." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Reset Button Released."           -- ENTERPRISE petevts 
   |--#TYPE       "Button/Switch Event" 
--#SUMMARY    "Reset Button Released." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 G"FRU latch Closed (Switch indicating FRU latch is in latched position)"           -- ENTERPRISE petevts 
   v--#TYPE       "Button/Switch Event" 
--#SUMMARY    "FRU latch Closed" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 %"FRU service request button Released"           -- ENTERPRISE petevts 
   �--#TYPE       "Button/Switch Event" 
--#SUMMARY    "FRU service request button Released" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Module/Board State Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Module/Board Event" 
--#SUMMARY    "Module/Board State Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Module/Board State Asserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Module/Board Event" 
--#SUMMARY    "Module/Board State Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ,"Module/Board Predictive Failure Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Module/Board Event" 
--#SUMMARY    "Module/Board Predictive Failure Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 *"Module/Board Predictive Failure Asserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Module/Board Event" 
--#SUMMARY    "Module/Board Predictive Failure Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ."Microcontroller/Coprocessor State Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Microcontroller/Coprocessor Event" 
--#SUMMARY    "Microcontroller/Coprocessor State Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ,"Microcontroller/Coprocessor State Asserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Microcontroller/Coprocessor Event" 
--#SUMMARY    "Microcontroller/Coprocessor State Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ;"Microcontroller/Coprocessor Predictive Failure Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Microcontroller/Coprocessor Event" 
--#SUMMARY    "Microcontroller/Coprocessor Predictive Failure Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 9"Microcontroller/Coprocessor Predictive Failure Asserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Microcontroller/Coprocessor Event" 
--#SUMMARY    "Microcontroller/Coprocessor Predictive Failure Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Add-in Card State Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Add-in Card Event" 
--#SUMMARY    "Add-in Card State Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Add-in Card State Asserted"           -- ENTERPRISE petevts 
   ~--#TYPE       "Add-in Card Event" 
--#SUMMARY    "Add-in Card State Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 +"Add-in Card Predictive Failure Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Add-in Card Event" 
--#SUMMARY    "Add-in Card Predictive Failure Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 )"Add-in Card Predictive Failure Asserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Add-in Card Event" 
--#SUMMARY    "Add-in Card Predictive Failure Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Chassis State Deasserted"           -- ENTERPRISE petevts 
   x--#TYPE       "Chassis Event" 
--#SUMMARY    "Chassis State Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Chassis State Asserted"           -- ENTERPRISE petevts 
   v--#TYPE       "Chassis Event" 
--#SUMMARY    "Chassis State Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 '"Chassis Predictive Failure Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Chassis Event" 
--#SUMMARY    "Chassis Predictive Failure Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 %"Chassis Predictive Failure Asserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Chassis Event" 
--#SUMMARY    "Chassis Predictive Failure Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Chip Set State Deasserted"           -- ENTERPRISE petevts 
   z--#TYPE       "Chip Set Event" 
--#SUMMARY    "Chip Set State Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Chip Set State Asserted"           -- ENTERPRISE petevts 
   x--#TYPE       "Chip Set Event" 
--#SUMMARY    "Chip Set State Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ("Chip Set Predictive Failure Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Chip Set Event" 
--#SUMMARY    "Chip Set Predictive Failure Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 &"Chip Set Predictive Failure Asserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Chip Set Event" 
--#SUMMARY    "Chip Set Predictive Failure Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 G"Chip Set did not respond to BMC request to change system power state."           -- ENTERPRISE petevts 
   u--#TYPE       "Chip Set Event" 
--#SUMMARY    "Soft Power Control Failure" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 "Thermal Trip Occured"           -- ENTERPRISE petevts 
   o--#TYPE       "Chip Set Event" 
--#SUMMARY    "Thermal Trip Occured" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 J"Chip Set started responding to BMC request to change system power state."           -- ENTERPRISE petevts 
   �--#TYPE       "Chip Set Event" 
--#SUMMARY    "Soft Power Control Failure Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Thermal Trip Cleared"           -- ENTERPRISE petevts 
   u--#TYPE       "Chip Set Event" 
--#SUMMARY    "Thermal Trip Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "FRU State Deasserted"           -- ENTERPRISE petevts 
   v--#TYPE       "Other FRU Event" 
--#SUMMARY    "FRU State Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "FRU State Asserted"           -- ENTERPRISE petevts 
   t--#TYPE       "Other FRU Event" 
--#SUMMARY    "FRU State Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 #"FRU Predictive Failure Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Other FRU Event" 
--#SUMMARY    "FRU Predictive Failure Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 !"FRU Predictive Failure Asserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Other FRU Event" 
--#SUMMARY    "FRU Predictive Failure Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 '"Cable / Interconnect State Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Other Cable / Interconnect Event" 
--#SUMMARY    "Cable / Interconnect State Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 %"Cable / Interconnect State Asserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Other Cable / Interconnect Event" 
--#SUMMARY    "Cable / Interconnect State Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 4"Cable / Interconnect Predictive Failure Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Other Cable / Interconnect Event" 
--#SUMMARY    "Cable / Interconnect Predictive Failure Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 2"Cable / Interconnect Predictive Failure Asserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Other Cable / Interconnect Event" 
--#SUMMARY    "Cable / Interconnect Predictive Failure Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 !"Cable/Interconnect is connected"           -- ENTERPRISE petevts 
   �--#TYPE       "Other Cable / Interconnect Event" 
--#SUMMARY    "Cable/Interconnect is connected" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 M"Configuration Error - Incorrect cable connected / Incorrect interconnection"           -- ENTERPRISE petevts 
   �--#TYPE       "Other Cable / Interconnect Event" 
--#SUMMARY    "Configuration Error" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 $"Cable/Interconnect is disconnected"           -- ENTERPRISE petevts 
   �--#TYPE       "Other Cable / Interconnect Event" 
--#SUMMARY    "Cable/Interconnect is disconnected" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 "Configuration Error Cleared"           -- ENTERPRISE petevts 
   �--#TYPE       "Other Cable / Interconnect Event" 
--#SUMMARY    "Configuration Error Cleared" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Terminator State Deasserted"           -- ENTERPRISE petevts 
   ~--#TYPE       "Terminator Event" 
--#SUMMARY    "Terminator State Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Terminator State Asserted"           -- ENTERPRISE petevts 
   |--#TYPE       "Terminator Event" 
--#SUMMARY    "Terminator State Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 *"Terminator Predictive Failure Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Terminator Event" 
--#SUMMARY    "Terminator Predictive Failure Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ("Terminator Predictive Failure Asserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Terminator Event" 
--#SUMMARY    "Terminator Predictive Failure Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 -"System Boot / Restart Initiated by power up"           -- ENTERPRISE petevts 
   �--#TYPE       "System Boot / Restart Event" 
--#SUMMARY    "System Boot / Restart Initiated by power up" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 /"System Boot / Restart Initiated by Hard Reset"           -- ENTERPRISE petevts 
   �--#TYPE       "System Boot / Restart Event" 
--#SUMMARY    "System Boot / Restart Initiated by Hard Reset" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 /"System Boot / Restart Initiated by Warm Reset"           -- ENTERPRISE petevts 
   �--#TYPE       "System Boot / Restart Event" 
--#SUMMARY    "System Boot / Restart Initiated by Warm Reset" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 1"System Boot / Restart - User requested PXE boot"           -- ENTERPRISE petevts 
   �--#TYPE       "System Boot / Restart Event" 
--#SUMMARY    "System Boot / Restart - User requested PXE boot" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 6"System Boot / Restart - Automatic boot to diagnostic"           -- ENTERPRISE petevts 
   �--#TYPE       "System Boot / Restart Event" 
--#SUMMARY    "System Boot / Restart - Automatic boot to diagnostic" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 E"System Boot / Restart - OS / run-time software initiated hard reset"           -- ENTERPRISE petevts 
   �--#TYPE       "System Boot / Restart Event" 
--#SUMMARY    "System Boot / Restart - OS / run-time software initiated hard reset" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 E"System Boot / Restart - OS / run-time software initiated Warm reset"           -- ENTERPRISE petevts 
   �--#TYPE       "System Boot / Restart Event" 
--#SUMMARY    "System Boot / Restart - OS / run-time software initiated Warm reset" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 L"System Boot / Restart - Restart cause per Get System Restart Cause command"           -- ENTERPRISE petevts 
   �--#TYPE       "System Boot / Restart Event" 
--#SUMMARY    "System Boot / Restart - Restart cause per Get System Restart Cause command" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 8"System Boot / Restart Initiated by power up Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE       "System Boot / Restart Event" 
--#SUMMARY    "System Boot / Restart Initiated by power up Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 :"System Boot / Restart Initiated by Hard Reset Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE       "System Boot / Restart Event" 
--#SUMMARY    "System Boot / Restart Initiated by Hard Reset Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 :"System Boot / Restart Initiated by Warm Reset Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE       "System Boot / Restart Event" 
--#SUMMARY    "System Boot / Restart Initiated by Warm Reset Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 <"System Boot / Restart - User requested PXE boot Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE       "System Boot / Restart Event" 
--#SUMMARY    "System Boot / Restart - User requested PXE boot Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 A"System Boot / Restart - Automatic boot to diagnostic Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE       "System Boot / Restart Event" 
--#SUMMARY    "System Boot / Restart - Automatic boot to diagnostic Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 P"System Boot / Restart - OS / run-time software initiated hard reset Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE       "System Boot / Restart Event" 
--#SUMMARY    "System Boot / Restart - OS / run-time software initiated hard reset Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 P"System Boot / Restart - OS / run-time software initiated Warm reset Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE       "System Boot / Restart Event" 
--#SUMMARY    "System Boot / Restart - OS / run-time software initiated Warm reset Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 W"System Boot / Restart - Restart cause per Get System Restart Cause command Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE       "System Boot / Restart Event" 
--#SUMMARY    "System Boot / Restart - Restart cause per Get System Restart Cause command Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
  "Boot Error - No bootable media"           -- ENTERPRISE petevts 
   |--#TYPE       "Boot Error Event" 
--#SUMMARY    "Boot Error - No bootable media" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 2"Boot Error - Non-bootable diskette left in drive"           -- ENTERPRISE petevts 
   �--#TYPE       "Boot Error Event" 
--#SUMMARY    "Boot Error - Non-bootable diskette left in drive" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 #"Boot Error - PXE Server not found"           -- ENTERPRISE petevts 
   --#TYPE       "Boot Error Event" 
--#SUMMARY    "Boot Error - PXE Server not found" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 ""Boot Error - Invalid boot sector"           -- ENTERPRISE petevts 
   ~--#TYPE       "Boot Error Event" 
--#SUMMARY    "Boot Error - Invalid boot sector" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 @"Boot Error - Timeout waiting for user selection of boot source"           -- ENTERPRISE petevts 
   �--#TYPE       "Boot Error Event" 
--#SUMMARY    "Boot Error - Timeout waiting for user selection of boot source" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Found bootable media"           -- ENTERPRISE petevts 
   w--#TYPE       "Boot Error Event" 
--#SUMMARY    "Found bootable media" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Bootable diskette Found"           -- ENTERPRISE petevts 
   z--#TYPE       "Boot Error Event" 
--#SUMMARY    "Bootable diskette Found" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "PXE Server found"           -- ENTERPRISE petevts 
   s--#TYPE       "Boot Error Event" 
--#SUMMARY    "PXE Server found" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Found valid boot sector"           -- ENTERPRISE petevts 
   z--#TYPE       "Boot Error Event" 
--#SUMMARY    "Found Valid boot sector" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "User selected boot source"           -- ENTERPRISE petevts 
   |--#TYPE       "Boot Error Event" 
--#SUMMARY    "User selected boot source" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "A: boot completed"           -- ENTERPRISE petevts 
   q--#TYPE       "OS Boot Event" 
--#SUMMARY    "A: boot completed" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "C: boot completed"           -- ENTERPRISE petevts 
   q--#TYPE       "OS Boot Event" 
--#SUMMARY    "C: boot completed" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "PXE boot completed"           -- ENTERPRISE petevts 
   r--#TYPE       "OS Boot Event" 
--#SUMMARY    "PXE boot completed" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Diagnostic boot completed"           -- ENTERPRISE petevts 
   y--#TYPE       "OS Boot Event" 
--#SUMMARY    "Diagnostic boot completed" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "CDROM boot completed"           -- ENTERPRISE petevts 
   t--#TYPE       "OS Boot Event" 
--#SUMMARY    "CDROM boot completed" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "ROM boot completed"           -- ENTERPRISE petevts 
   r--#TYPE       "OS Boot Event" 
--#SUMMARY    "ROM boot completed" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ,"Boot completed - boot device not specified"           -- ENTERPRISE petevts 
   �--#TYPE       "OS Boot Event" 
--#SUMMARY    "Boot completed - boot device not specified" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "A: boot incomplete"           -- ENTERPRISE petevts 
   l--#TYPE       "OS Boot Event" 
--#SUMMARY    "A: boot incomplete" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 "C: boot incomplete"           -- ENTERPRISE petevts 
   l--#TYPE       "OS Boot Event" 
--#SUMMARY    "C: boot incomplete" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 "PXE boot Incomplete"           -- ENTERPRISE petevts 
   m--#TYPE       "OS Boot Event" 
--#SUMMARY    "PXE boot Incomplete" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 "Diagnostic boot Incomplete"           -- ENTERPRISE petevts 
   t--#TYPE       "OS Boot Event" 
--#SUMMARY    "Diagnostic boot Incomplete" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 "CDROM boot Incomplete"           -- ENTERPRISE petevts 
   o--#TYPE       "OS Boot Event" 
--#SUMMARY    "CDROM boot Incomplete" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 "ROM boot Incomplete"           -- ENTERPRISE petevts 
   m--#TYPE       "OS Boot Event" 
--#SUMMARY    "ROM boot Incomplete" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 -"Boot Incomplete - boot device not specified"           -- ENTERPRISE petevts 
   �--#TYPE       "OS Boot Event" 
--#SUMMARY    "Boot Incomplete - boot device not specified" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 �"OS Stop / Shutdown - Stop during OS load / initialization. Unexpected error uring system startup. Stopped waiting for input or power cycle/reset"           -- ENTERPRISE petevts 
   �--#TYPE       "OS Stop / Shutdown Event" 
--#SUMMARY    "OS Stop / Shutdown - Stop during OS load / initialization" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 -"OS Stop / Shutdown - Run-time Critical Stop"           -- ENTERPRISE petevts 
   �--#TYPE       "OS Stop / Shutdown Event" 
--#SUMMARY    "OS Stop / Shutdown - Run-time Critical Stop" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 �"OS Stop / Shutdown - Graceful Stop (system powered up, but normal OS operation has shut down and system is awaiting reset pushbutton, powercycle or other external input)"           -- ENTERPRISE petevts 
   �--#TYPE       "OS Stop / Shutdown Event" 
--#SUMMARY    "OS Stop / Shutdown - Graceful Stop" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 K"OS Stop / Shutdown - Graceful Shutdown (system graceful power down by OS)"           -- ENTERPRISE petevts 
   �--#TYPE       "OS Stop / Shutdown Event" 
--#SUMMARY    "OS Stop / Shutdown - Graceful Shutdown" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 5"OS Stop / Shutdown - Soft Shutdown initiated by PEF"           -- ENTERPRISE petevts 
   �--#TYPE       "OS Stop / Shutdown Event" 
--#SUMMARY    "OS Stop / Shutdown - Soft Shutdown initiated by PEF" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 +"OS Stop / Shutdown - Agent Not Responding"           -- ENTERPRISE petevts 
   �--#TYPE       "OS Stop / Shutdown Event" 
--#SUMMARY    "OS Stop / Shutdown - Agent Not Responding" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 -"OS Stop / Shutdown - power cycle/reset Done"           -- ENTERPRISE petevts 
   �--#TYPE       "OS Stop / Shutdown Event" 
--#SUMMARY    "OS Stop / Shutdown - Stop during OS load / initialization Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ,"OS Stop / Shutdown -Power Cycle/Reset Done"           -- ENTERPRISE petevts 
   �--#TYPE       "OS Stop / Shutdown Event" 
--#SUMMARY    "OS Stop / Shutdown - Run-time INFORMATIONAL Stop Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 `"OS Stop / Shutdown - System powered up by reset pushbutton, powercycle or other external input"           -- ENTERPRISE petevts 
   �--#TYPE       "OS Stop / Shutdown Event" 
--#SUMMARY    "OS Stop / Shutdown - Graceful Stop Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ]"OS Stop / Shutdown - System powered by reset pushbutton, powercycle or other external input"           -- ENTERPRISE petevts 
   �--#TYPE       "OS Stop / Shutdown Event" 
--#SUMMARY    "OS Stop / Shutdown - Graceful Shutdown Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ]"OS Stop / Shutdown - System powered by reset pushbutton, powercycle or other external input"           -- ENTERPRISE petevts 
   �--#TYPE       "OS Stop / Shutdown Event" 
--#SUMMARY    "OS Stop / Shutdown - Soft Shutdown Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 /"OS Stop / Shutdown - Agent Started Responding"           -- ENTERPRISE petevts 
   �--#TYPE       "OS Stop / Shutdown Event" 
--#SUMMARY    "OS Stop / Shutdown - Agent Started Responding" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 *"Slot / Connector - Fault Status asserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Fault Status asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 -"Slot / Connector - Identify Status asserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Identify Status asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ."Slot / Connector - Device installed/attached"           -- ENTERPRISE petevts 
   �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Device installed/attached" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 d"Slot / Connector - Ready for Device Installation. Typically, this means that the slot power is off"           -- ENTERPRISE petevts 
   �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Ready for Device Installation" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 _"Slot / Connector - Ready for Device Removal. Typically, this means that the slot power is off"           -- ENTERPRISE petevts 
   �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Ready for Device Removal" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 &"Slot / Connector - Slot Power is Off"           -- ENTERPRISE petevts 
   �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Slot Power is Off" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 +"Slot / Connector - Device Removal Request"           -- ENTERPRISE petevts 
   �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Device Removal Request" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 '"Slot / Connector - Interlock asserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Interlock asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Slot / Connector - Disabled"           -- ENTERPRISE petevts 
   �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Disabled" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 '"Slot / Connector - holds spare device"           -- ENTERPRISE petevts 
   �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - holds spare device" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ,"Slot / Connector - Fault Status Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Fault Status Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 /"Slot / Connector - Identify Status Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Identify Status Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 /"Slot / Connector - Device Uninstalled/Removed"           -- ENTERPRISE petevts 
   �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Device Uninstalled/Removed" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 g"Slot / Connector - Not Ready for Device Installation. Typically, this means that the slot power is on"           -- ENTERPRISE petevts 
   �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Not Ready for Device Installation" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 b"Slot / Connector - Not Ready for Device Removal. Typically, this means that the slot power is on"           -- ENTERPRISE petevts 
   �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Ready for Device Removal" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 %"Slot / Connector - Slot Power is On"           -- ENTERPRISE petevts 
   �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Slot Power is On" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 5"Slot / Connector - Device Removal Request Processed"           -- ENTERPRISE petevts 
   �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Device Removal Request Processed" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 )"Slot / Connector - Interlock Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Interlock Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Slot / Connector - Enabled"           -- ENTERPRISE petevts 
   �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - Enabled" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 '"Slot / Connector - frees spare device"           -- ENTERPRISE petevts 
   �--#TYPE       "Slot / Connector Event" 
--#SUMMARY    "Slot / Connector - frees spare device" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 -"System ACPI Power State - S0 / G0 - Working"           -- ENTERPRISE petevts 
   �--#TYPE       "System ACPI Power State Event" 
--#SUMMARY    "System ACPI Power State - S0 / G0 " 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 X"System ACPI Power State - S1 - sleeping with system h/w & processor context maintained"           -- ENTERPRISE petevts 
   �--#TYPE       "System ACPI Power State Event" 
--#SUMMARY    "System ACPI Power State - S1" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ?"System ACPI Power State - S2 sleeping, processor context lost"           -- ENTERPRISE petevts 
   �--#TYPE       "System ACPI Power State Event" 
--#SUMMARY    "System ACPI Power State - S2 " 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "System ACPI Power State - S3"           -- ENTERPRISE petevts 
   �--#TYPE       "System ACPI Power State Event" 
--#SUMMARY    "System ACPI Power State - S3 - sleeping, processor & h/w context lost, memory retained" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 E"System ACPI Power State - S4 - non-volatile sleep / suspend-to disk"           -- ENTERPRISE petevts 
   �--#TYPE       "System ACPI Power State Event" 
--#SUMMARY    "System ACPI Power State - S4" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ."System ACPI Power State - S5 / G2 - soft-off"           -- ENTERPRISE petevts 
   �--#TYPE       "System ACPI Power State Event" 
--#SUMMARY    "System ACPI Power State - S5 / G2" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 X"System ACPI Power State - S4 / S5 soft-off, particular S4 / S5 state cannot be determi"           -- ENTERPRISE petevts 
   �--#TYPE       "System ACPI Power State Event" 
--#SUMMARY    "System ACPI Power State - S4 / S5 soft-off" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 /"System ACPI Power State - G3 - Mechanical Off"           -- ENTERPRISE petevts 
   �--#TYPE       "System ACPI Power State Event" 
--#SUMMARY    "System ACPI Power State - G3" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ?"System ACPI Power State - Sleeping in an S1, S2, or S3 states"           -- ENTERPRISE petevts 
   �--#TYPE       "System ACPI Power State Event" 
--#SUMMARY    "System ACPI Power State - Sleeping in an S1, S2, or S3 states" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 L"System ACPI Power State - G1 - sleeping (S1-S4 state cannot be determined)"           -- ENTERPRISE petevts 
   �--#TYPE       "System ACPI Power State Event" 
--#SUMMARY    "System ACPI Power State - G1" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 2"System ACPI Power State - S5 entered by override"           -- ENTERPRISE petevts 
   �--#TYPE       "System ACPI Power State Event" 
--#SUMMARY    "System ACPI Power State - S5 entered by override" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 +"System ACPI Power State - Legacy ON state"           -- ENTERPRISE petevts 
   �--#TYPE       "System ACPI Power State Event" 
--#SUMMARY    "System ACPI Power State - Legacy ON state" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ,"System ACPI Power State - Legacy OFF state"           -- ENTERPRISE petevts 
   �--#TYPE       "System ACPI Power State Event" 
--#SUMMARY    "System ACPI Power State - Legacy OFF state" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 #"System ACPI Power State - Unknown"           -- ENTERPRISE petevts 
   �--#TYPE       "System ACPI Power State Event" 
--#SUMMARY    "System ACPI Power State - Unknown" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ?"Watchdog timer expired, status only (no action, no interrupt)"           -- ENTERPRISE petevts 
   q--#TYPE       "Watchdog Event" 
--#SUMMARY    "Watchdog timer expired" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 "Watchdog Reset"           -- ENTERPRISE petevts 
   j--#TYPE       "Watchdog Event" 
--#SUMMARY    "Watchdog Reset" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "Watchdog Power Down"           -- ENTERPRISE petevts 
   o--#TYPE       "Watchdog Event" 
--#SUMMARY    "Watchdog Power Down" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "Watchdog Power Cycle"           -- ENTERPRISE petevts 
   o--#TYPE       "Watchdog Event" 
--#SUMMARY    "Watchdog Power cycle" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 "Watchdog Timer interrupt"           -- ENTERPRISE petevts 
   y--#TYPE       "Watchdog Event" 
--#SUMMARY    "Watchdog Timer interrupt" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Watchdog timer Reset"           -- ENTERPRISE petevts 
   o--#TYPE       "Watchdog Event" 
--#SUMMARY    "Watchdog timer reset" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 "Watchdog Reset Deasserted"           -- ENTERPRISE petevts 
   u--#TYPE       "Watchdog Event" 
--#SUMMARY    "Watchdog Reset Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
  "Watchdog Power Down Deasserted"           -- ENTERPRISE petevts 
   z--#TYPE       "Watchdog Event" 
--#SUMMARY    "Watchdog Power Down Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 !"Watchdog Power Cycle Deasserted"           -- ENTERPRISE petevts 
   z--#TYPE       "Watchdog Event" 
--#SUMMARY    "Watchdog Power cycle Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 %"Watchdog Timer interrupt Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Watchdog Event" 
--#SUMMARY    "Watchdog Timer interrupt Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 *"Platform Alert - platform generated page"           -- ENTERPRISE petevts 
   �--#TYPE       "Platform Alert Event" 
--#SUMMARY    "Platform Alert- platform generated page" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 /"Platform Alert - platform generated LAN alert"           -- ENTERPRISE petevts 
   �--#TYPE       "Platform Alert Event" 
--#SUMMARY    "Platform Alert- platform generated LAN alert" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 0"Platform Alert - Platform Event Trap generated"           -- ENTERPRISE petevts 
   �--#TYPE       "Platform Alert Event" 
--#SUMMARY    "Platform Alert-  Platform Event Trap generated (formatted per IPMI PET specification)" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ;"Platform Alert - platform generated SNMP trap, OEM format"           -- ENTERPRISE petevts 
   �--#TYPE       "Platform Alert Event" 
--#SUMMARY    "Platform Alert- platform generated SNMP trap, OEM format" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 )"A device is absent or has been removed."           -- ENTERPRISE petevts 
   �--#TYPE       "Entity Presence Event" 
--#SUMMARY    "A device is absent or has been removed." 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 +"A device is present or has been inserted."           -- ENTERPRISE petevts 
   �--#TYPE       "Entity Presence Event" 
--#SUMMARY    "A device is present or has been inserted." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 C"The Entity identified by the Entity ID for the sensor is present."           -- ENTERPRISE petevts 
   v--#TYPE       "Entity Presence Event" 
--#SUMMARY    "Entity Present" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 B"The Entity identified by the Entity ID for the sensor is Absent."           -- ENTERPRISE petevts 
   v--#TYPE       "Entity Presence Event" 
--#SUMMARY    "Entity Absent." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 D"The Entity identified by the Entity ID for the sensor is Disabled."           -- ENTERPRISE petevts 
   x--#TYPE       "Entity Presence Event" 
--#SUMMARY    "Entity Disabled." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 &"Monitor ASIC / IC Failure Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Monitor ASIC / IC Event" 
--#SUMMARY    "Monitor ASIC / IC Failure Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 $"Monitor ASIC / IC Failure Asserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Monitor ASIC / IC Event" 
--#SUMMARY    "Monitor ASIC / IC Failure Asserted" 
--#ARGUMENTS  {} 
--#SEVERITY   MAJOR 
 '"Sensor access degraded or unavailable"           -- ENTERPRISE petevts 
   �--#TYPE       "Management Subsystem Health Event" 
--#SUMMARY    "Sensor access degraded or unavailable" 
--#ARGUMENTS  {} 
--#SEVERITY   MAJOR 
 +"Controller access degraded or unavailable"           -- ENTERPRISE petevts 
   �--#TYPE       "Management Subsystem Health Event" 
--#SUMMARY    "Controller access degraded or unavailable" 
--#ARGUMENTS  {} 
--#SEVERITY   MAJOR 
  "Management controller off-line"           -- ENTERPRISE petevts 
   �--#TYPE       "Management Subsystem Health Event" 
--#SUMMARY    "Management controller off-line" 
--#ARGUMENTS  {} 
--#SEVERITY   MAJOR 
 #"Management controller Unavailable"           -- ENTERPRISE petevts 
   �--#TYPE       "Management Subsystem Health Event" 
--#SUMMARY    "Management controller Unavailable" 
--#ARGUMENTS  {} 
--#SEVERITY   MAJOR 
 "Sensor failure"           -- ENTERPRISE petevts 
   z--#TYPE       "Management Subsystem Health Event" 
--#SUMMARY    "Sensor failure" 
--#ARGUMENTS  {} 
--#SEVERITY   MAJOR 
 "FRU failure"           -- ENTERPRISE petevts 
   w--#TYPE       "Management Subsystem Health Event" 
--#SUMMARY    "FRU failure" 
--#ARGUMENTS  {} 
--#SEVERITY   MAJOR 
 "Sensor access Available"           -- ENTERPRISE petevts 
   �--#TYPE       "Management Subsystem Health Event" 
--#SUMMARY    "Sensor access Available" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Controller access Available"           -- ENTERPRISE petevts 
   �--#TYPE       "Management Subsystem Health Event" 
--#SUMMARY    "Controller access Available" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Management controller online"           -- ENTERPRISE petevts 
   �--#TYPE       "Management Subsystem Health Event" 
--#SUMMARY    "Management controller online" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 !"Management controller Available"           -- ENTERPRISE petevts 
   �--#TYPE       "Management Subsystem Health Event" 
--#SUMMARY    "Management controller Available" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Sensor failure Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Management Subsystem Health Event" 
--#SUMMARY    "Sensor failure Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "FRU failure Deasserted"           -- ENTERPRISE petevts 
   �--#TYPE       "Management Subsystem Health Event" 
--#SUMMARY    "FRU failure Deasserted" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Battery low"           -- ENTERPRISE petevts 
   e--#TYPE       "Battery Event" 
--#SUMMARY    "Battery low" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 "Battery Failed"           -- ENTERPRISE petevts 
   i--#TYPE       "Battery Event" 
--#SUMMARY    "Battery Failed" 
--#ARGUMENTS  {} 
--#SEVERITY   CRITICAL 
 "Battery presence detected"           -- ENTERPRISE petevts 
   y--#TYPE       "Battery Event" 
--#SUMMARY    "Battery presence detected" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Session Activated"           -- ENTERPRISE petevts 
   w--#TYPE       "Session Audit Event" 
--#SUMMARY    "Session Activated" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "Session Deactivated"           -- ENTERPRISE petevts 
   s--#TYPE       "Session Audit Event" 
--#SUMMARY    "Session Deactivated" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 &"Session Invalid Username or Password"           -- ENTERPRISE petevts 
   �--#TYPE       "Session Audit Event" 
--#SUMMARY    "Session Invalid Username or Password" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 L"A user's access has been disabled due to a series of bad password attempts"           -- ENTERPRISE petevts 
   �--#TYPE       "Session Audit Event" 
--#SUMMARY    "Session Invalid password disable" 
--#ARGUMENTS  {} 
--#SEVERITY   WARNING 
 9"Hardware Version change detected with associated Entity"           -- ENTERPRISE petevts 
   �--#TYPE       "Version Change Event" 
--#SUMMARY    "Hardware Version change detected" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 E"Firmware or Software version change detected with associated Entity"           -- ENTERPRISE petevts 
   �--#TYPE       "Version Change Event" 
--#SUMMARY    "Firmware or Software version change detected" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 9"Hardware Incombabaility detected with associated Entity"           -- ENTERPRISE petevts 
   �--#TYPE       "Version Change Event" 
--#SUMMARY    "Hardware Incombabaility detected" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 N"Firmware Or Software Version Incompatibility detected with associated Entity"           -- ENTERPRISE petevts 
   �--#TYPE       "Version Change Event" 
--#SUMMARY    "Firmware Or SoftwareVersion Incompatibility detected" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 9"Entity is of an invalid or unsupported hardware version"           -- ENTERPRISE petevts 
   �--#TYPE       "Version Change Event" 
--#SUMMARY    "Entity is of an invalid or unsupported hardware version" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 H"Entity contains an invalid or unsupported firmware or software version"           -- ENTERPRISE petevts 
   �--#TYPE       "Version Change Event" 
--#SUMMARY    "Entity contains an invalid or unsupported firmware or software version" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 @"Hardware Change detected with associated Entity was successful"           -- ENTERPRISE petevts 
   �--#TYPE       "Version Change Event" 
--#SUMMARY    "Hardware Change detected with associated Entity was successful" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 H"Software or F/W Change detected with associated Entity was successful."           -- ENTERPRISE petevts 
   �--#TYPE       "Version Change Event" 
--#SUMMARY    "Software or F/W Change detected with associated Entity was successful." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 D"Hardware Change detected with associated Entity was not successful"           -- ENTERPRISE petevts 
   �--#TYPE       "Version Change Event" 
--#SUMMARY    "Hardware Change detected with associated Entity was not successful" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 L"Software or F/W Change detected with associated Entity was not successful."           -- ENTERPRISE petevts 
   �--#TYPE       "Version Change Event" 
--#SUMMARY    "Software or F/W Change detected with associated Entity was not successful." 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "FRU Not Installed"           -- ENTERPRISE petevts 
   s--#TYPE       "FRU State Event" 
--#SUMMARY    "FRU Not Installed" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "FRU Inactive"           -- ENTERPRISE petevts 
   n--#TYPE       "FRU State Event" 
--#SUMMARY    "FRU Inactive" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "FRU Activation Requested"           -- ENTERPRISE petevts 
   z--#TYPE       "FRU State Event" 
--#SUMMARY    "FRU Activation Requested" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "FRU Activation In Progress"           -- ENTERPRISE petevts 
   |--#TYPE       "FRU State Event" 
--#SUMMARY    "FRU Activation In Progress" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "FRU Active"           -- ENTERPRISE petevts 
   l--#TYPE       "FRU State Event" 
--#SUMMARY    "FRU Active" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "FRU Deactivation Requested"           -- ENTERPRISE petevts 
   |--#TYPE       "FRU State Event" 
--#SUMMARY    "FRU Deactivation Requested" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "FRU Deactivation In Progress"           -- ENTERPRISE petevts 
   ~--#TYPE       "FRU State Event" 
--#SUMMARY    "FRU Deactivation In Progress" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 "FRU Communication Lost"           -- ENTERPRISE petevts 
   x--#TYPE       "FRU State Event" 
--#SUMMARY    "FRU Communication Lost" 
--#ARGUMENTS  {} 
--#SEVERITY   INFORMATIONAL 
 ""CPU0 Channel0 Dimm0 memory Error"           -- ENTERPRISE petevts 
     ""CPU0 Channel0 Dimm1 memory Error"           -- ENTERPRISE petevts 
     ""CPU0 Channel0 Dimm2 memory Error"           -- ENTERPRISE petevts 
     ""CPU0 Channel1 Dimm0 memory Error"           -- ENTERPRISE petevts 
     ""CPU0 Channel1 Dimm1 memory Error"           -- ENTERPRISE petevts 
     ""CPU0 Channel1 Dimm2 memory Error"           -- ENTERPRISE petevts 
     ""CPU0 Channel2 Dimm0 memory Error"           -- ENTERPRISE petevts 
     ""CPU0 Channel2 Dimm1 memory Error"           -- ENTERPRISE petevts 
     ""CPU0 Channel2 Dimm2 memory Error"           -- ENTERPRISE petevts 
     ""CPU0 Channel3 Dimm0 memory Error"           -- ENTERPRISE petevts 
     ""CPU0 Channel3 Dimm1 memory Error"           -- ENTERPRISE petevts 
     ""CPU0 Channel3 Dimm2 memory Error"           -- ENTERPRISE petevts 
     ""CPU1 Channel0 Dimm0 memory Error"           -- ENTERPRISE petevts 
     ""CPU1 Channel0 Dimm1 memory Error"           -- ENTERPRISE petevts 
     ""CPU1 Channel0 Dimm2 memory Error"           -- ENTERPRISE petevts 
     ""CPU1 Channel1 Dimm0 memory Error"           -- ENTERPRISE petevts 
     ""CPU1 Channel1 Dimm1 memory Error"           -- ENTERPRISE petevts 
     ""CPU1 Channel1 Dimm2 memory Error"           -- ENTERPRISE petevts 
     ""CPU1 Channel2 Dimm0 memory Error"           -- ENTERPRISE petevts 
     ""CPU1 Channel2 Dimm1 memory Error"           -- ENTERPRISE petevts 
     ""CPU1 Channel2 Dimm2 memory Error"           -- ENTERPRISE petevts 
     ""CPU1 Channel3 Dimm0 memory Error"           -- ENTERPRISE petevts 
     ""CPU1 Channel3 Dimm1 memory Error"           -- ENTERPRISE petevts 
     ""CPU1 Channel3 Dimm2 memory Error"           -- ENTERPRISE petevts 
     !"CPU0 Bus and interconnect Error"           -- ENTERPRISE petevts 
     "CPU0 L3 Tag Error"           -- ENTERPRISE petevts 
     "CPU0 Internal Error"           -- ENTERPRISE petevts 
     !"CPU1 Bus and interconnect Error"           -- ENTERPRISE petevts 
     "CPU1 L3 Tag Error"           -- ENTERPRISE petevts 
     "CPU1 Internal Error"           -- ENTERPRISE petevts 
     !"CPU2 Bus and interconnect Error"           -- ENTERPRISE petevts 
     "CPU2 L3 Tag Error"           -- ENTERPRISE petevts 
     "CPU2 Internal Error"           -- ENTERPRISE petevts 
     !"CPU3 Bus and interconnect Error"           -- ENTERPRISE petevts 
     "CPU3 L3 Tag Error"           -- ENTERPRISE petevts 
     "CPU3 Internal Error"           -- ENTERPRISE petevts 
        