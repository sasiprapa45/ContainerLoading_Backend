import matplotlib.pyplot as plt

# def plot(boxes, con, frame_index):
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')

#     container = con[frame_index]
#     container_id = container['id']
#     ax.bar3d(0, 0, 0, container['length'], container['width'], container['height'], shade=True, alpha=0.1)

#     filtered_boxes = filter(lambda box: box.conid == container_id, boxes)
#     for box in filtered_boxes:
#         width = box.width
#         height = box.height
#         depth = box.depth
#         x, y, z, n = box.position  # ตำแหน่ง
#         print(box.cargoid)
#         ax.bar3d(x, y, z, depth, width, height, shade=False, alpha=0.8, edgecolor='k')

#     # กำหนดค่าแกน
#     ax.set_xlim3d(0, 1000)
#     ax.set_ylim3d(0, 1000)
#     ax.set_zlim3d(0, 1000)
#     plt.axis('off')
#     plt.show()
    
# def Plot_boxes(boxes, con):
#     for i in range(len(con)):
#         plot(boxes, con, i)
    
    # w,d,h ของกล่องปัจจุบัน rx,ry,rz,np ของตำแหย่งที่จะตั้ง w1,d1,h1,rx1,ry1,rz1,n1 ของกล่องที่ตั้งไปแล้ว con_length, con_width, con_height คอนเทรนเนอรของตำแหน่ง
def ch_verlap(w,d,h,rx,ry,rz,w1,d1,h1,rx1,ry1,rz1,np,n1, con_length, con_width, con_height):
    # ตรวจสอบว่ากล่อง  ซ้อนทับกันหรือไม่
    if np != n1:
        return False
    elif d + rx > con_length or w + ry > con_width or h + rz > con_height: # เต็มตู้ com ยัง
        return True
    elif  (rx < rx1 + d1 and rx + d > rx1 and
        rz < rz1 + h1 and rz + h>rz1 and
        ry < ry1 + w1 and ry + w>ry1) and np == n1:
        return True
    else :
        # print("ไม่ชน")
        return False

# เลือก  conน้อยสุด ลึกสุด ซ้ายสุด ต่ำสุด
def sortpo(p):
    return (p[3], p[0], p[2],p[1])

def fitness(l, lo, n, cargoes_c):
    f1 = float(0.9 * float(12)/(n+1)) #N แปรผกพันกับ f1
    f2 = float(1 / float(1 + float(l / lo)) ) #L0 คือความกว้างของคอนเทนเนอร  L คือความยาวการบรรจุในคอนเทนเนอรใบสุดทาย
    f = (f1 + (0.1*f2) ) + cargoes_c
    return f

class Box:
    def __init__(self, depth, width, height, position, cargoid, conid):
        self.width = width
        self.height = height
        self.depth = depth
        self.position = position  # ตำแหน่งจัดกล่อง
        self.cargoid = cargoid
        self.conid = conid
        
class BoxData:
    def __init__(self, x, y, z, cargoes_id, container_id):
        self.x = x
        self.y = y
        self.z = z
        self.cargoes_id = cargoes_id
        self.container_id = container_id


def Placement(box,cont) : #หาค่า fitness
    con = cont
    boxes=[]
    p = []
    boxes_data = []
    for i in range(len(box)):
        # print("กล่องที่ ",i,"ขนาด ",box[i])
        # print(box[i])
        d = box[i]['length']
        w = box[i]['width']
        h = box[i]['height']
        caid = box[i]['id']
        container_found = False  # ใช้ตัวแปรนี้เพื่อตรวจสอบว่าพบ container ที่เหมาะสมหรือไม่
        for n in range(len(con)):
            if len(boxes) == 0 or not any(box.conid == con[n]['id'] for box in boxes):
                boxes.append(Box(d, w, h, (0, 0, 0, n), caid, con[n]['id']))
                p.append((0, w + 0, 0, n))
                p.append((0 + d, 0, 0, n))
                p.append((0, 0, 0 + h, n))
                boxes_data.append(BoxData(0,0,0,caid,con[n]['id']))
                container_found = True
                break
            else:
                for j in range(len(p)):  # ตำแหน่งว่างต่อ
                    r = p[j]  #คือตำแหน่งต่อกล่อง
                    rx = r[0] #ความลึก ความยาว
                    ry = r[1] #ความกว้าง
                    rz = r[2] #ความสูง
                    np = r[3] #เลขตู้คอน
                    cp = 0  #ตรวจสอบ
                    if d + rx > con[n]['length'] or w + ry > con[n]['width'] or h + rz > con[n]['height']: # เต็มตู้ com ยัง
                        cp += 1
                    else:
                        for m in range(len(boxes)):#หาตำแหน่งที่ต่อ
                        # print("วางตำแหน่ง ",p[j],"ตรวจกับกล่องที่ ",m)
                            w1 = boxes[m].width
                            h1 = boxes[m].height
                            d1 = boxes[m].depth
                            rx1, ry1, rz1, n1 = boxes[m].position[0], boxes[m].position[1], boxes[m].position[2],boxes[m].position[3]
                            if ch_verlap(w, d, h, rx, ry, rz, w1, d1, h1, rx1, ry1, rz1, np, n1, con[np]['length'], con[np]['width'], con[np]['height'] ):
                                cp += 1
                    if cp == 0:
                        boxes.append(Box(d, w, h, (rx, ry, rz, np), caid, con[np]['id']))
                        boxes_data.append(BoxData(rx,ry,rz,caid,con[np]['id']))
                        p.append((rx, w + ry, rz, np)) #ต่อซ้าย
                        p.append((rx + d, ry, rz, np)) #ต่อด้านหน้า
                        p.append((rx, ry, rz + h, np)) #ต่อบน
                        p.sort(key=sortpo)
                        p.remove((rx, ry, rz, np))
                        container_found = True
                        break  # Exit the loop after placing the box in a container
                if container_found:
                    # print(i)
                    break  # Exit the loop after placing the box in a container
        if not container_found:
            # No available space in any container, break or continue here as needed
            break
    # for boxs in boxes:
    #     print(boxs.depth,boxs.width,boxs.height,boxs.position,boxs.cargoid,boxs.conid)
    max_n = max(boxes, key=lambda x: x.position[3]).position[3]
    max_box = max(boxes, key=lambda x: (x.position[3], x.depth + x.position[0]))
    cargoes_c = len(boxes)
    # print(cargoes_c)
    # print('max_n')
    # print(max_n)
    # print('max_box.depth + max_box.position[0]')
    # print(max_box.depth + max_box.position[0])
    fit = fitness((max_box.depth + max_box.position[0]), con[max_n]['width'], max_n+1, cargoes_c)
    # print("fitness; ")
    # print(fit)
    return boxes_data,fit,boxes

