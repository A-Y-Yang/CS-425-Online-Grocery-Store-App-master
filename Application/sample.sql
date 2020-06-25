insert into customer(customer_id, first_name, last_name, phone, email, payment_total, paid_total, da_line_one, da_line_two, da_city, da_state, da_zipcode) 
values (nextval('customer_id_sq'),'Mary','Watson','3123344125','maryw@gmail.com',0,0,'123 Sun St.','Apt 2B','Hoover','AL','33241'),
        (nextval('customer_id_sq'),'Ben','Li','1239344125','benli@gmail.com',0,0,'2839 N Brown Ave','Basement','Hoover','AL','33228'),
        (nextval('customer_id_sq'),'Rose','Jackson','3123124528','rose.j@gmail.com',0,0,'215 SUNSHINE ST','APT 4H','CHICAGO','IL','60611'),
        (nextval('customer_id_sq'),'Kate','Ye','7283344333','katey@yahoo.com',0,0,'2940 Silver Pl',null,'Evanston','IL','62309'),
        (nextval('customer_id_sq'),'Shirley','Adams','8271093344','sa@int.com',0,0,'142 Clart St.','Apt 1A','Chicago','IL','61284');
--break
insert into staff 
values (nextval('staff_id_sq'),'Alice','Leasly','439 Gold Dr.','Apt 2F','Chicago','IL','61928','7739182182','alice@g3.com',100000,'Senior Manager'),
        (nextval('staff_id_sq'),'Jennie','Fairwood','92 N Seew Pl','Apt 1H','Chicago','IL','60573','3122849181','jenniew@g3.com',75000,'Manager'),
        (nextval('staff_id_sq'),'Will','Smith','3891 N Mile Drive','Coachhouse','Hoover','AL','33899','8272938714','will@g3.com',300000,'COO'),
        (nextval('staff_id_sq'),'Andrews','Brown','312 Redway St.','Ln 1','Naperville','IL','68291','2849281239','andrews@g3.com',35000,'Store Administrator'),
        (nextval('staff_id_sq'),'Sonja','LeRondo','9201 S Yoer Street',null,'Oak Park','IL','62839','5482981020','sonja@g3.com',30000,'Store Operator');
--break
insert into supplier 
values (nextval('supplier_id_sq'),'ABC Supplier','8271002222','abc@gmail.com','1122-1250 Hoover Ct',null,'Hoover','AL','33111'),
        (nextval('supplier_id_sq'),'ChiTown Supplier','7737737733','chitown@gmail.com','728 W Rood Ave','#1555','Chicago','IL','68888');

--break
insert into credit_card 
values (1234123412341234,'Mary Watson','1123','311','123 Sun St.','Apt 2B','Hoover','AL','33241'),
        (9876987698769876,'Mary Watson','0724','829','123 Sun St.','Apt 2B','Hoover','AL','33241'),
        (5500223344772299,'Rose L. Jackson','0123','935','215 SUNSHINE ST','APT 4H','CHICAGO','IL','60611'),
        (3829199918882555,'Rose Jackson','0526','748','215 SUNSHINE ST','APT 4H','CHICAGO','IL','60611'),
        (7788119922662266,'Ken Jackson','0325','748','215 SUNSHINE ST','APT 4H','CHICAGO','IL','60611');
--break
insert into category 
values (nextval('category_id_seq'),'Food'),
        (nextval('category_id_seq'),'Alcoholic Beverages'),
        (nextval('category_id_seq'),'Non-alcoholic Beverages');
--break
insert into product 
values (nextval('product_id_sq'),'Orange',0.78,0.001,'Nutrition facts: calories 62, fat 0 g, cholesterol 0 mg, sodium 0 mg, total carbohydrate 15 g, dietary fiber 3 g, sugars 12 g, added sugars 0 g, protein 1 g, vitamin d 0%%, calcium 5%%, iron 0%%, potassium 7%%',1,'orange.jpeg'),
        (nextval('product_id_sq'),'Banana',0.49,0.002,'Nutrition facts: calories 105, fat 0 g, cholesterol 0 mg, sodium 0 mg, total carbohydrate 27 g, dietary fiber 3 g, sugars 14 g, added sugars 0 g, protein 1 g, vitamin d 0%%, calcium 1%%, iron 0%%, potassium 13%%',1,'banana.jpg'),
        (nextval('product_id_sq'),'Antinori Villa Toscana 2016',23.99,0.66,'750ML / 13.5%% ABV',2,'redwine_1.jpg'),
        (nextval('product_id_sq'),'Whole Milk',1.79,0.02,'Nutrition facts: calories 150, fat 8 g, cholesterol 30 mg, sodium 120 mg, total carbohydrate 12 g, dietary fiber 0 g, sugars 12 g, added sugars 0 g, protein 8 g, vitamin d 0%%, calcium 30%%, iron 0%%, potassium 8%%',3,'milk.jpeg'),
        (nextval('product_id_sq'),'Cold Brew Coffee (can)',2.79,0.001,'Nutrition facts: calories 5, fat 0 g, cholesterol 0 mg, sodium 25 mg, total carbohydrate 3 g, dietary fiber 2 g, sugars 0 g, added sugars 0 g, protein 0 g, vitamin d 0%%, calcium 2%%, iron 0%%, potassium 0%%',3,'coffee.jpg');
--break
insert into orders 
values (nextval('order_id_sq'),1000001,'1234123412341234',4.39,'2020-06-22 18:24:02','received'),
        (nextval('order_id_sq'),1000003,'5500223344772299',4.39,'2020-06-23 09:29:03','send'),
        (nextval('order_id_sq'),1000003,'7788119922662266',4.39,'2020-06-24 11:10:35','send'),
        (nextval('order_id_sq'),1000001,'9876987698769876',4.39,'2020-06-24 22:44:20','send');
--break
insert into warehouse(warehouse_id, name, a_line_one, a_line_two, a_city, a_state, a_zipcode, capacity, capacity_used) 
values (nextval('warehouse_id_sq'),'CHI Warehouse','1000-1820 W Sun Ave','#2222','Chicago','IL','60382',20000,0),
        (nextval('warehouse_id_sq'),'Hoover Warehouse','293-380 Happy Pl',null,'Hoover','AL','33411',35000.893,0);
--break
insert into supplier_item 
values (8000001,3000001,0.5),
        (8000001,3000002,0.45),
        (8000002,3000003,21.49),
        (8000002,3000001,0.4),
        (8000001,3000005,1.49);
--break
insert into product_price 
values (3000001,'IL',0.89),
        (3000002,'IL',0.59),
        (3000003,'AL',24.79),
        (3000001,'AL',0.78),
        (3000002,'AL',0.49),
        (3000005,'IL',2.49);
--break
insert into stock 
values (3000001,9000001,1000,1000*0.001),
        (3000002,9000001,60,60*0.002),
        (3000003,9000002,10,10*0.66),
        (3000002,9000002,20,20*0.002),
        (3000005,9000001,20,20*0.001);
--break
insert into add_stock 
values (2000001,3000001,9000001,1000,1000*0.001),
        (2000001,3000002,9000001,10,10*0.002),
        (2000002,3000003,9000002,10,10*0.66),
        (2000003,3000002,9000002,20,20*0.002),
        (2000002,3000005,9000001,20,20*0.001);
--break
insert into availability 
values (3000001,9000001,1000),
        (3000002,9000001,60),
        (3000003,9000002,10),
        (3000002,9000002,20),
        (3000005,9000001,20);
--break
insert into owns 
values (1000001,'1234123412341234'),
        (1000001,'9876987698769876'),
        (1000003,'5500223344772299'),
        (1000003,'3829199918882555'),
        (1000003,'7788119922662266');
--break
insert into order_item(order_id,product_id,quantity,unit_price) 
values (5000001,3000001,5,0.78),
        (5000001,3000002,1,0.49),
        (5000002,3000005,10,2.49),
        (5000003,3000001,3,0.89),
        (5000003,3000002,2,0.59),
        (5000004,3000003,2,24.79);
--break