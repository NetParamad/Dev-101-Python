import ipaddress
from tabulate import tabulate

def allocate_subnets(base_network: str, host_requirements: list, router_links: int = 0):
    """
    จัดสรร Subnet ตามจำนวน Host ที่ต้องการในแต่ละเครือข่ายย่อย และกำหนด IP ระหว่าง Router
    :param base_network: เครือข่ายหลัก (เช่น '169.128.8.0/21')
    :param host_requirements: รายชื่อจำนวนโฮสต์ในแต่ละ Subnet (เช่น [380, 61, 60, 33, 30, 5, 5, 5])
    :param router_links: จำนวนลิงก์ระหว่างเราเตอร์ (เช่น 3)
    """
    
    # รวมจำนวน Host ที่ต้องการ (รวมลิงก์ระหว่างเราเตอร์)
    host_requirements.extend([2] * router_links)
    
    # จัดเรียงจำนวน Host จากมากไปน้อย
    host_requirements.sort(reverse=True)
    
    # สร้างเครือข่ายหลักจาก Base Network
    network = ipaddress.ip_network(base_network, strict=False)
    
    # เก็บผลลัพธ์
    allocated_subnets = []
    
    # เริ่มต้นจัดสรร Subnet
    available_subnets = [network]
    
    for idx, hosts in enumerate(host_requirements, start=1):
        # คำนวณจำนวน IP ที่ต้องการ (รวม Network และ Broadcast)
        required_ips = hosts + 2
        for subnet in available_subnets:
            if subnet.num_addresses >= required_ips:
                # คำนวณ Subnet Mask ที่เหมาะสม
                new_prefix = 32 - (required_ips - 1).bit_length()
                allocated_subnet = list(subnet.subnets(new_prefix=new_prefix))[0]
                
                subnet_type = "Router Link" if hosts == 2 else f"Host {hosts}"
                
                allocated_subnets.append([
                    idx,
                    subnet_type,
                    str(allocated_subnet.network_address),
                    f"/{allocated_subnet.prefixlen}",
                    str(allocated_subnet.netmask),
                    f"{str(list(allocated_subnet.hosts())[0])} - {str(list(allocated_subnet.hosts())[-1])}",
                    str(allocated_subnet.broadcast_address),
                    allocated_subnet.num_addresses - 2,
                ])
                
                # อัปเดต Subnet ที่ยังไม่ได้ใช้งาน
                available_subnets.remove(subnet)
                available_subnets.extend(subnet.address_exclude(allocated_subnet))
                break
        else:
            print(f"ไม่สามารถจัดสรรเครือข่ายให้กับ {hosts} hosts ได้")
    
    return allocated_subnets

# ข้อมูลการจัดสรรเครือข่าย
base_network = '169.128.8.0/21'
host_requirements = [380, 61, 60, 33, 30, 5, 5, 5]  # จำนวน Host ที่ต้องการ
router_links = 3  # จำนวนลิงก์ระหว่างเราเตอร์ (A-B, A-C, A-D)

# เรียกใช้ฟังก์ชันเพื่อจัดสรรเครือข่าย
allocated = allocate_subnets(base_network, host_requirements, router_links)

# แสดงผลลัพธ์ในรูปแบบตาราง
headers = ["#", "Type", "Network", "Prefix", "Subnet Mask", "Usable IP Range", "Broadcast", "Total Hosts"]
print(tabulate(allocated, headers=headers, tablefmt="grid"))