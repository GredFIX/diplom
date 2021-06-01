CREATE TABLE IF NOT EXISTS instructors (
	lgn VARCHAR(30) PRIMARY KEY,
	last_name VARCHAR(20) NOT NULL,
	first_name VARCHAR(20) NOT NULL,
	middle_name VARCHAR(20), 
	phone VARCHAR(15) NOT NULL,
	pwd TEXT NOT NULL 
);

CREATE TABLE IF NOT EXISTS schedule (
	num_group VARCHAR(10) PRIMARY KEY,
	lgn VARCHAR(30) REFERENCES instructors ON DELETE SET NULL,
	mon VARCHAR(5),
	tue VARCHAR(5),
	wed VARCHAR(5),
	thu VARCHAR(5),
	fri VARCHAR(5),
	sat VARCHAR(5),
	sun VARCHAR(5)
);

CREATE TABLE IF NOT EXISTS students (
	lgn VARCHAR(30) PRIMARY KEY,
	last_name VARCHAR(20) NOT NULL,
	first_name VARCHAR(20) NOT NULL,
	middle_name VARCHAR(20),
	num_group VARCHAR(10) REFERENCES schedule ON DELETE SET NULL,
	test_1 SMALLINT CHECK (test_1>=0 and test_1<=100),
	test_2 SMALLINT CHECK (test_2>=0 and test_2<=100),
	test_3 SMALLINT CHECK (test_3>=0 and test_3<=100),
	phone VARCHAR(15) NOT NULL,
	pwd TEXT NOT NULL 
);

INSERT INTO instructors (lgn, last_name, first_name, middle_name, phone, pwd) VALUES 
('t_ivanov', 'Иванов', 'Михаил', 'Cеменович','+79101112233', '4d4ecd4f0258c40ad71d06b9fc40773dad99f49e90a56e84a1a7d06f6b2f516c:d287233db4ef4a68ba3fd138d5bd9df3'),
('t_makarov', 'Макаров', 'Олег', 'Артурович','+79062222222', 'efa7cead7dedd9539fbdc973765a4e6a677800515624c28ddc65bbb435cc253e:f92222c7a73f4938b798fec63ded2864'),
('t_nosov', 'Носов', 'Дмитрий', NULL,'+79024444444', '9d02267b3d5f004eee875e3d45731578944b0a9ce117cafdb2d4b241318b7c32:27c545ff1bbf47be91eaac4d8e0f6e26'),
('t_petrov', 'Петров', 'Андрей', 'Артемович','+79161234567', 'c8e2d57f0d869e5d06295eb09d18292be713396b72dbe6aa68f200571540472f:e7d8b28a0ebe4029a1d0f81e22193e10');

INSERT INTO schedule (num_group, lgn, mon, tue,	wed, thu, fri, sat,	sun)
VALUES
('BA-1','t_ivanov','17:30','17:30','17:30','17:30','17:30', NULL, NULL),
('BA-2','t_makarov','17:30', NULL,'17:30',NULL,'17:30', NULL, NULL),
('BM-1','t_nosov', NULL,'17:30',NULL,'17:30',NULL, NULL, NULL),
('BM-2','t_ivanov', NULL, NULL, NULL, NULL, NULL, '17:30','17:30');

INSERT INTO students (lgn, last_name, first_name, middle_name, phone, num_group, pwd, test_1, test_2, test_3) VALUES 
('st_djabrailov','Джабраилов', 'Арсен', 'Арсенович','+79101232123','BA-1','5df092cdafaa559d2bbdfc247c7349236dd6b63bcb1b22be73330b606811d4e3:a75a45bd2d8c45af8e740d58fbd42174', 20, 90, 20),
('st_mixaylov','Михайлов', 'Олег', NULL,'+79153334455','BM-1','ebcfdcd5895b3489f7001ee1ff75a90583c470d74cdb2845a7f243056db9b25f:dfad1d095f4b4320af87e7b790c9248f', 50, 21, 31),
('st_egorov','Егоров', 'Никита', 'Сергеевич','+79027777777','BA-1','566895ce79cdbbacb1bcc870e000726094e7c9d5422a677e34b0e06829c0d74c:8d6d68451bc14051bc494fa134bf57ea', 25, 22, 32),
('st_kuzmin','Кузьмин', 'Сергей', 'Иванович','+79101232222','BA-2','5f39a515fbecb5f0e82c20a068625a0703db3484c086fcc63673b15a3a78307c:7f0d213fd38c40fc9f3273ede9a854ea', NULL, 90, NULL),
('st_petrov','Петров', 'Михаил', NULL,'+79153338823','BM-1','cb1320e62457ecb4a692c26cc4ff2225c9bfd85f0568dbe131ad62c404dd1520:fe31b7d9fc454f2fa50ad703c1831376', 50, 21, 31),
('st_ivanov','Иванов', 'Дмитрий', 'Петрович','+749511656','BA-2','54219cc636097d6fa1a7cc5377f4202783375d8187d41e73c4848e82c4a7f19c:c1749018b1b94fd1841abedea21375ce', 24, 22, 32),
('st_kostenko','Костенко', 'Геннадий', 'Иванович','+79101233333','BA-2','b6b815dd25c605b4d1ad0a0df0c7b1b81afe3ca29e6261436d31fafd340a548f:592037acbce7418a930d6a9160bb7535', 55, 90, NULL),
('st_li','Ли', 'Олег', NULL,'+79153331190','BM-2','38c6df82413a24854344d11de9c00ee8bce6b8d75a94721259d4d1b68e2a5d3a:e347e3f7826d43a391c4faa4500d0ed6', 50, 21, 31),
('st_yagoda','Ягода', 'Никита', 'Петрович','+79164504545','BA-1','50a51024f4decc17b1e8961887ec03523113a6659ea67436d0aabbe95c609671:80f22f067bcc4a57be4cbf76a873d83e', 47, 22, 32),
('st_pushkin','Пушкин', 'Кирилл', 'Иванович','+79101256192','BA-1','7d8575577156d3ec4d99fbf45b59b4dceb952202736e9540890a177fd5dfad49:2c568074855141d7a002ae830b986b52', 10, 90, 100),
('st_putin','Путин', 'Константин', 'Никитович','+79771183478','BM-2','3337c45148d5c3d86dd021a77b6389863a34b01b6cbfe93a7c3cb513382ccde3:eb77e1edd5104ac0bd62a0c3e9b3e1cc', 45, 13, 23);