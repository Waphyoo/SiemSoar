

# 1. Add Rule On dashboard

![alt text](image-6.png)

![alt text](image-7.png)

![alt text](image.png)

![alt text](image-1.png)

![alt text](image-2.png)

![alt text](image-3.png)

![alt text](image-4.png)


**Log มี `program_name: '2example'`** แต่กลับ **match กับ rule 100010** ที่มี `<program_name>example</program_name>`

นี่แสดงให้เห็นว่า:

### `<program_name>` ใน Wazuh ทำ **Substring/Contains Match**

```
program_name: "2example"
↓
ตรวจสอบว่ามี substring "example" อยู่ไหม? → ✓ YES
↓
Match rule 100010
```

**ไม่ใช่ exact match อย่างที่ผมบอกผิดไป!**

## ทำไม Rule 100012 ไม่ match?

เพราะ **Wazuh ใช้หลัก "First Match Wins"**:

1. ประเมิน rule 100010 → `program_name` มี "example" → **Match แล้ว!**
2. หยุดการประเมิน → ไม่ไป evaluate rule 100012 อีก
3. ถึง rule 100012 จะ match ด้วย "2example" แต่ Wazuh หยุดแล้วที่ rule แรก

![alt text](image-8.png)

![alt text](image-5.png)

## สรุป

1. ย้าย rule ที่ละเอียดกว่าอยู่ข้างบน
2. ต้องไม่ต้อง restart manager ก่อน ก็สามารถ logtest ได้
3. ต้อง restart manager ก่อน ถึงจะได้ alert จาก rule นั้น


![alt text](image-22.png)


# 2. Add rule by API



![alt text](image-9.png)

![alt text](image-11.png)

![alt text](image-12.png)

![alt text](image-13.png)

![alt text](image-14.png)

https://www.freeformatter.com/json-escape.html#before-output

![alt text](image-15.png)


![alt text](image-10.png)

![alt text](image-17.png)

![alt text](image-18.png)

![alt text](image-16.png)

![alt text](image-30.png)

![alt text](image-19.png)

![alt text](image-20.png)

![alt text](image-21.png)


# 3. script python

![alt text](image-27.png)

Wazuh Indexer users (internal users) - ผู้ใช้ที่อยู่ใน database ของ Wazuh Indexer

Wazuh Server API users - ผู้ใช้สำหรับเข้าถึง Wazuh Manager API

- ใช้ admin: default administrator account of the Wazuh indexer ในการ call wazuh api ไม่ได้

![alt text](image-23.png)

![alt text](image-24.png)

![alt text](image-25.png)

![alt text](image-26.png)

![alt text](image-29.png)

![alt text](image-28.png)











