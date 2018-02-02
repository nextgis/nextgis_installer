# Intro

Mac OS X qemu/kvm worker on Ubuntu 16.04 LTS Server.

# Prepare

For Ubuntu 16.04 LTS server

main instructions: https://github.com/kholia/OSX-KVM
get seabios 1.10 here: https://launchpad.net/~panfaust/+archive/ubuntu/qemu-backports
get qemu 2.9 here: https://launchpad.net/~pmdj/+archive/ubuntu/qemu-ppa

# Config

Success config looks like

```xml
<!--
WARNING: THIS IS AN AUTO-GENERATED FILE. CHANGES TO IT ARE LIKELY TO BE
OVERWRITTEN AND LOST. Changes to this xml configuration should be made using:
  virsh edit build-mac
or other application using the libvirt API.
-->

<domain type='kvm' xmlns:qemu='http://libvirt.org/schemas/domain/qemu/1.0'>
  <name>build-mac</name>
  <uuid>dbd4ca8a-1c90-4019-a423-151f6b9ed519</uuid>
  <title>build-mac</title>
  <description># echo 1 &gt; /sys/module/kvm/parameters/ignore_msrs</description>
  <memory unit='KiB'>6275072</memory>
  <currentMemory unit='KiB'>4194304</currentMemory>
  <vcpu placement='static'>8</vcpu>
  <os>
    <type arch='x86_64' machine='pc-q35-2.4'>hvm</type>
    <kernel>/var/lib/libvirt/iso/enoch_rev2902_boot</kernel>
  </os>
  <features>
    <acpi/>
    <kvm>
      <hidden state='on'/>
    </kvm>
  </features>
  <cpu mode='custom' match='exact'>
    <model fallback='allow'>Penryn</model>
  </cpu>
  <clock offset='utc'/>
  <on_poweroff>destroy</on_poweroff>
  <on_reboot>restart</on_reboot>
  <on_crash>destroy</on_crash>
  <devices>
    <emulator>/usr/bin/qemu-system-x86_64</emulator>
    <disk type='file' device='disk'>
      <driver name='qemu' type='qcow2'/>
      <source file='/var/lib/libvirt/images/mac_hdd.qcow2'/>
      <target dev='sda' bus='sata'/>
      <boot order='1'/>
      <address type='drive' controller='0' bus='0' target='0' unit='0'/>
    </disk>
    <controller type='usb' index='0' model='ich9-ehci1'>
      <address type='pci' domain='0x0000' bus='0x01' slot='0x1d' function='0x7'/>
    </controller>
    <controller type='usb' index='0' model='ich9-uhci1'>
      <master startport='0'/>
      <address type='pci' domain='0x0000' bus='0x01' slot='0x1d' function='0x0' multifunction='on'/>
    </controller>
    <controller type='usb' index='0' model='ich9-uhci2'>
      <master startport='2'/>
      <address type='pci' domain='0x0000' bus='0x01' slot='0x1d' function='0x1'/>
    </controller>
    <controller type='usb' index='0' model='ich9-uhci3'>
      <master startport='4'/>
      <address type='pci' domain='0x0000' bus='0x01' slot='0x1d' function='0x2'/>
    </controller>
    <controller type='sata' index='0'>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x1f' function='0x2'/>
    </controller>
    <controller type='pci' index='0' model='pcie-root'/>
    <controller type='pci' index='1' model='dmi-to-pci-bridge'>
      <model name='i82801b11-bridge'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x1e' function='0x0'/>
    </controller>
    <controller type='pci' index='2' model='pci-bridge'>
      <model name='pci-bridge'/>
      <target chassisNr='2'/>
      <address type='pci' domain='0x0000' bus='0x01' slot='0x01' function='0x0'/>
    </controller>
    <interface type='network'>
      <mac address='52:54:00:da:52:41'/>
      <source network='default'/>
      <model type='e1000-82545em'/>
      <address type='pci' domain='0x0000' bus='0x02' slot='0x02' function='0x0'/>
    </interface>
    <input type='tablet' bus='usb'>
      <address type='usb' bus='0' port='1'/>
    </input>
    <input type='mouse' bus='ps2'/>
    <input type='keyboard' bus='ps2'/>
    <graphics type='spice' autoport='yes' listen='192.168.250.1' keymap='en-us'>
      <listen type='address' address='192.168.250.1'/>
    </graphics>
    <video>
      <model type='vmvga' vram='16384' heads='1'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x01' function='0x0'/>
    </video>
    <memballoon model='none'/>
  </devices>
  <qemu:commandline>
    <qemu:arg value='-usb'/>
    <qemu:arg value='-device'/>
    <qemu:arg value='usb-tablet,bus=usb-bus.0'/>
    <qemu:arg value='-device'/>
    <qemu:arg value='usb-kbd,bus=usb-bus.0'/>
    <qemu:arg value='-device'/>
    <qemu:arg value='isa-applesmc,osk=ourhardworkbythesewordsguardedpleasedontsteal(c)AppleComputerInc'/>
    <qemu:arg value='-smbios'/>
    <qemu:arg value='type=2'/>
    <qemu:arg value='-k'/>
    <qemu:arg value='en-us'/>
    <qemu:arg value='-cpu'/>
    <qemu:arg value='Penryn,vendor=GenuineIntel'/>
    <qemu:arg value='-device'/>
    <qemu:arg value='ide-drive,bus=ide.1,drive=MacDVD'/>
    <qemu:arg value='-drive'/>
    <qemu:arg value='id=MacDVD,if=none,snapshot=on,file=/var/lib/libvirt/iso/Install_OS_X_Sierra.iso'/>
  </qemu:commandline>
</domain>
```
