-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: shopgiaydep22112025
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cthoadon`
--

DROP TABLE IF EXISTS `cthoadon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cthoadon` (
  `MaHD` varchar(40) NOT NULL,
  `MaSP` varchar(30) NOT NULL,
  `TenSP` varchar(300) NOT NULL,
  `MauSac` varchar(100) NOT NULL,
  `Size` varchar(50) NOT NULL,
  `SoLuongMua` int NOT NULL,
  `DonGia` decimal(14,2) NOT NULL,
  `ThanhTien` decimal(16,2) NOT NULL,
  PRIMARY KEY (`MaHD`,`MaSP`,`MauSac`,`Size`),
  KEY `MaSP` (`MaSP`),
  CONSTRAINT `cthoadon_ibfk_1` FOREIGN KEY (`MaHD`) REFERENCES `hoadon` (`MaHD`),
  CONSTRAINT `cthoadon_chk_1` CHECK ((`SoLuongMua` >= 0)),
  CONSTRAINT `cthoadon_chk_2` CHECK ((`DonGia` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cthoadon`
--

LOCK TABLES `cthoadon` WRITE;
/*!40000 ALTER TABLE `cthoadon` DISABLE KEYS */;
INSERT INTO `cthoadon` VALUES ('HD001','SP001','Nike Metcon 9 By You','Đen','41',1,4999000.00,4999000.00),('HD001','SP002','Giày Streettalk','Trắng','42',2,1200000.00,2400000.00),('HD003','SP001','Nike Metcon 9 By You','Trắng','42',1,4999000.00,4999000.00),('HD003','SP002','Giày Streettalk','Trắng','43',3,1200000.00,3600000.00),('HD004','SP001','Nike Metcon 9 By You','Xanh dương','43',1,4999000.00,4999000.00),('HD005','SP002','Giày Streettalk','Trắng','44',1,1200000.00,1200000.00),('HD006','SP002','Giày Streettalk','Trắng','42',2,1200000.00,2400000.00),('HD007','SP001','Nike Metcon 9 By You','Xanh dương','41',1,4999000.00,4999000.00),('HD008','SP001','Nike Metcon 9 By You','Đen','42',1,4999000.00,4999000.00),('HD009','SP002','Giày Streettalk','Trắng','43',2,1200000.00,2400000.00),('HD010','SP001','Nike Metcon 9 By You','Trắng','44',1,4999000.00,4999000.00),('HD010','SP002','Giày Streettalk','Trắng','42',1,1200000.00,1200000.00),('HD011','SP001','Nike Metcon 9 By You','Mặc định','Mặc định',1,4999000.00,4999000.00),('HD011','SP002','Giày Streettalk','Mặc định','Mặc định',1,1200000.00,1200000.00),('HD012','SP001','Nike Metcon 9 By You','Mặc định','Mặc định',1,4999000.00,4999000.00),('HD012','SP002','Giày Streettalk','Mặc định','Mặc định',1,1200000.00,1200000.00),('HD013','SP001','Nike Metcon 9 By You','Mặc định','Mặc định',1,4999000.00,4999000.00),('HD013','SP002','Giày Streettalk','Mặc định','Mặc định',1,1200000.00,1200000.00),('HD014','SP001','Nike Metcon 9 By You','Mặc định','Mặc định',1,4999000.00,4999000.00),('HD014','SP002','Giày Streettalk','Mặc định','Mặc định',1,1200000.00,1200000.00),('HD015','SP001','Nike Metcon 9 By You','Mặc định','Mặc định',1,4999000.00,4999000.00),('HD015','SP002','Giày Streettalk','Mặc định','Mặc định',1,1200000.00,1200000.00),('HD016','SP001','Nike Metcon 9 By You','Mặc định','Mặc định',2,4999000.00,9998000.00),('HD016','SP002','Giày Streettalk','Mặc định','Mặc định',1,1200000.00,1200000.00),('HD017','SP002','Giày Streettalk','Mặc định','Mặc định',1,1200000.00,1200000.00),('HD018','SP001','Nike Metcon 9 By You','Mặc định','Mặc định',1,4999000.00,4999000.00),('HD018','SP002','Giày Streettalk','Mặc định','Mặc định',1,1200000.00,1200000.00),('HD019','SP001','Nike Metcon 9 By You','Trắng','42',1,4999000.00,4999000.00),('HD020','SP001','Nike Metcon 9 By You','Đen','42',8,4999000.00,39992000.00),('HD020','SP001','Nike Metcon 9 By You','Trắng','42',10,4999000.00,49990000.00),('HD020','SP002','Giày Streettalk','Đen','40',3,1200000.00,3600000.00),('HD020','SP002','Giày Streettalk','Nâu','37',1,1200000.00,1200000.00),('HD021','SP001','Nike Metcon 9 By You','Đen','42',76,4999000.00,379924000.00),('HD025','SP004','giày đè tem','Khô gà','42',1,1200000.00,1200000.00),('HD026','SP001','Nike Metcon 9 By You','Xanh Dương','43',3,4999000.00,14997000.00),('HD026','SP002','Giày Streettalk','Nâu','37',5,1200000.00,6000000.00),('HD026','SP003','Giày Handball Special','Nâu','42',6,2500000.00,15000000.00),('HD027','SP003','Giày Handball Special','Đen','41',10,2500000.00,25000000.00),('HD028','SP002','Giày Streettalk','Trắng','42',95,1200000.00,114000000.00),('HD029','SP002','Giày Streettalk','Đen','39',10,1200000.00,12000000.00),('HD030','SP003','Giày Handball Special','Trắng','42',13,2500000.00,32500000.00),('HD031','SP003','Giày Handball Special','Đen','42',100,2500000.00,250000000.00),('HD032','SP002','Giày Streettalk','Đen','42',1,1200000.00,1200000.00),('HD032','SP003','Giày Handball Special','Trắng','38',1,2500000.00,2500000.00),('HD032','SP004','giày đè tem','Đỏ','42',5,1200000.00,6000000.00),('HD032','SP004','giày đè tem','Xanh Dương','45',1,1200000.00,1200000.00),('HD033','SP003','Giày Handball Special','Đen','42',50,4500000.00,225000000.00),('HD034','SP003','Giày Handball Special','Đen','42',5,4500000.00,22500000.00),('HD035','SP003','Giày Handball Special','Nâu','37',5,2500000.00,12500000.00),('HD036','SP002','Giày Streettalk','Nâu','38',1,1200000.00,1200000.00),('HD036','SP003','Giày Handball Special','Xanh Dương','36',1,2500000.00,2500000.00),('HD036','SP003','Giày Handball Special','Xanh Dương','37',1,2500000.00,2500000.00),('HD037','SP002','Giày Streettalk','Trắng','45',4,1200000.00,4800000.00),('HD038','SP002','Giày Streettalk','Đen','42',1,1200000.00,1200000.00),('HD039','SP002','Giày Streettalk','Nâu','36',5,1200000.00,6000000.00),('HD039','SP003','Giày Handball Special','Nâu','42',3,2500000.00,7500000.00),('HD039','SP004','giày đè tem','Đen','36',5,1200000.00,6000000.00),('HD040','SP002','Giày Streettalk','Đen','42',2,1200000.00,2400000.00),('HD040','SP002','Giày Streettalk','Trắng','45',5,1200000.00,6000000.00),('HD041','SP001','Nike Metcon 9 By You','Trắng','36',1,4999000.00,4999000.00),('HD041','SP002','Giày Streettalk','Đen','42',1,1200000.00,1200000.00),('HD042','SP004','giày đè tem','Đen','42',1,1080000.00,1080000.00),('HD043','SP004','giày đè tem','Đen','42',1,1080000.00,1080000.00),('HD044','SP002','Giày Streettalk','Nâu','39',1,1200000.00,1200000.00),('HD045','SP005','ok','Đen','42',4,1000.00,4000.00),('HD046','SP002','Giày Streettalk','Đen','42',3,1200000.00,3600000.00),('HD046','SP003','Giày Handball Special','Đen','42',1,2500000.00,2500000.00);
/*!40000 ALTER TABLE `cthoadon` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donhang`
--

DROP TABLE IF EXISTS `donhang`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `donhang` (
  `MaDH` varchar(30) NOT NULL,
  `MaKH` varchar(30) NOT NULL,
  `NgayLap` datetime DEFAULT NULL,
  PRIMARY KEY (`MaDH`),
  KEY `donhang_ibfk_1` (`MaKH`),
  CONSTRAINT `donhang_ibfk_1` FOREIGN KEY (`MaKH`) REFERENCES `khachhang` (`MaKH`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donhang`
--

LOCK TABLES `donhang` WRITE;
/*!40000 ALTER TABLE `donhang` DISABLE KEYS */;
INSERT INTO `donhang` VALUES ('GH001','KH001',NULL),('GH002','KH002',NULL),('GH003','KH003',NULL),('GH004','KH004',NULL),('GH005','KH005',NULL),('GH006','KH006',NULL),('GH007','KH007',NULL),('GH008','KH008',NULL),('GH009','KH009',NULL),('GH010','KH010',NULL),('GH013','KH013',NULL),('GH015','KH011',NULL),('GH016','KH014','2025-11-22 19:21:31');
/*!40000 ALTER TABLE `donhang` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `giohangchuasanpham`
--

DROP TABLE IF EXISTS `giohangchuasanpham`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `giohangchuasanpham` (
  `MaKH` varchar(30) NOT NULL COMMENT 'Mã khách hàng - tham chiếu đến bảng khachhang',
  `MaSP` varchar(30) NOT NULL COMMENT 'Mã sản phẩm',
  `MauSac` varchar(100) NOT NULL COMMENT 'Màu sắc sản phẩm',
  `Size` varchar(20) NOT NULL COMMENT 'Kích cỡ sản phẩm',
  `SoLuong` int NOT NULL COMMENT 'Số lượng sản phẩm trong giỏ',
  PRIMARY KEY (`MaKH`,`MaSP`,`MauSac`,`Size`),
  KEY `MaSP` (`MaSP`),
  CONSTRAINT `giohangchuasanpham_ibfk_1` FOREIGN KEY (`MaKH`) REFERENCES `khachhang` (`MaKH`) ON DELETE CASCADE,
  CONSTRAINT `giohangchuasanpham_ibfk_2` FOREIGN KEY (`MaSP`) REFERENCES `sanpham` (`MaSP`) ON DELETE CASCADE,
  CONSTRAINT `giohangchuasanpham_chk_1` CHECK ((`SoLuong` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Giỏ hàng tạm - Lưu sản phẩm trước khi tạo đơn hàng';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `giohangchuasanpham`
--

LOCK TABLES `giohangchuasanpham` WRITE;
/*!40000 ALTER TABLE `giohangchuasanpham` DISABLE KEYS */;
/*!40000 ALTER TABLE `giohangchuasanpham` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hoadon`
--

DROP TABLE IF EXISTS `hoadon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hoadon` (
  `MaHD` varchar(40) NOT NULL,
  `MaKH` varchar(30) NOT NULL,
  `MaNV` varchar(30) DEFAULT NULL,
  `NgayLap` date DEFAULT NULL,
  PRIMARY KEY (`MaHD`),
  KEY `MaKH` (`MaKH`),
  KEY `MaNV` (`MaNV`),
  CONSTRAINT `hoadon_ibfk_1` FOREIGN KEY (`MaKH`) REFERENCES `khachhang` (`MaKH`),
  CONSTRAINT `hoadon_ibfk_2` FOREIGN KEY (`MaNV`) REFERENCES `nhanvien` (`MaNV`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hoadon`
--

LOCK TABLES `hoadon` WRITE;
/*!40000 ALTER TABLE `hoadon` DISABLE KEYS */;
INSERT INTO `hoadon` VALUES ('HD001','KH001','B23DCCN143','2025-10-09'),('HD002','KH002','B23DCCN302','2025-10-09'),('HD003','KH003','B23DCCN452','2025-10-09'),('HD004','KH004','B23DCCN898','2025-10-09'),('HD005','KH005','B23DCCN926','2025-10-09'),('HD006','KH006','B23DCCN143','2025-10-09'),('HD007','KH007','B23DCCN302','2025-10-09'),('HD008','KH008','B23DCCN452','2025-10-09'),('HD009','KH009','B23DCCN898','2025-10-09'),('HD010','KH010','B23DCCN926','2025-10-09'),('HD011','KH012',NULL,'2025-10-15'),('HD012','KH012',NULL,'2025-10-15'),('HD013','KH012',NULL,'2025-10-16'),('HD014','KH012',NULL,'2025-10-16'),('HD015','KH014',NULL,'2025-10-16'),('HD016','KH014',NULL,'2025-10-16'),('HD017','KH014',NULL,'2025-10-16'),('HD018','KH013',NULL,'2025-10-16'),('HD019','KH014',NULL,'2025-10-16'),('HD020','KH014',NULL,'2025-10-17'),('HD021','KH014',NULL,'2025-10-17'),('HD022','KH014',NULL,'2025-10-17'),('HD023','KH014',NULL,'2025-10-17'),('HD024','KH013',NULL,'2025-10-17'),('HD025','KH014',NULL,'2025-10-28'),('HD026','KH014',NULL,'2025-10-28'),('HD027','KH014',NULL,'2025-10-28'),('HD028','KH014',NULL,'2025-10-28'),('HD029','KH014',NULL,'2025-10-28'),('HD030','KH014',NULL,'2025-10-28'),('HD031','KH014',NULL,'2025-10-28'),('HD032','KH014',NULL,'2025-10-28'),('HD033','KH014',NULL,'2025-10-28'),('HD034','KH014',NULL,'2025-10-28'),('HD035','KH014',NULL,'2025-10-29'),('HD036','KH014',NULL,'2025-10-29'),('HD037','KH014',NULL,'2025-10-29'),('HD038','KH014',NULL,'2025-10-29'),('HD039','KH011',NULL,'2025-10-29'),('HD040','KH014',NULL,'2025-11-22'),('HD041','KH014',NULL,'2025-11-22'),('HD042','KH014',NULL,'2025-11-22'),('HD043','KH014',NULL,'2025-11-22'),('HD044','KH014',NULL,'2025-11-22'),('HD045','KH014',NULL,'2025-11-22'),('HD046','KH014',NULL,'2025-11-22');
/*!40000 ALTER TABLE `hoadon` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `khachhang`
--

DROP TABLE IF EXISTS `khachhang`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `khachhang` (
  `MaKH` varchar(30) NOT NULL,
  `TenKH` varchar(200) NOT NULL,
  `SDT` varchar(11) NOT NULL,
  `DiaChi` varchar(300) DEFAULT NULL,
  `TenDN` varchar(100) NOT NULL,
  `MatKhau` varchar(255) NOT NULL,
  PRIMARY KEY (`MaKH`),
  UNIQUE KEY `SDT` (`SDT`),
  UNIQUE KEY `TenDN` (`TenDN`),
  CONSTRAINT `khachhang_chk_1` CHECK (regexp_like(`SDT`,_utf8mb4'^[0-9]{10,11}$')),
  CONSTRAINT `khachhang_chk_2` CHECK ((char_length(`MatKhau`) >= 6))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `khachhang`
--

LOCK TABLES `khachhang` WRITE;
/*!40000 ALTER TABLE `khachhang` DISABLE KEYS */;
INSERT INTO `khachhang` VALUES ('KH001','Nguyễn Văn Bảo','0912345678','Bảo Nhai - Lào Cai','nguyenvanbao','abc123'),('KH002','Vũ Minh Dương','0987654321','Vũ Dương - Ninh Bình','vuminhduong','87654321'),('KH003','Trần Quang Hà','0901122334','Hà Đông - Hà Nội','tranquangha','1234567'),('KH004','Phạm Thị Hòa','0933445566','Yên Hòa - Hà Nội','phamthihoa','hoamai89'),('KH005','Đỗ Văn Nghĩa','0977223344','Yên Nghĩa - Hà Nội','dovannghia','nghia1234'),('KH006','Lê Thị Minh','0922334455','Tân Minh - Hải Phòng','lethiminh','minh567'),('KH007','Hoàng Anh Tuấn','0966889900','Bảo Thắng - Lào Cai','hoanganhtuan','tuantuan'),('KH008','Nguyễn Thị Lan','0944556677','Bắc Hà - Lào Cai','nguyenthilan','lan9999'),('KH009','Bùi Văn Hùng','09119992233','Hà Đông - Hà Nội','buivanhung','hung12345'),('KH010','Trần Thị Mai','0988112233','Vũ Dương - Ninh Bình','tranthimai','maimandinh'),('KH011','dinh son tung','0912334456','123 sđs','tungds2701','12345678'),('KH012','dinh son tung','0123456789','aloha','sontung','12345678'),('KH013','son tung mtp','0912323436','hoang mai ha noi','tung','12345678'),('KH014','tung son','0912006233','dai kim','mtp','12345678');
/*!40000 ALTER TABLE `khachhang` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mausac_sp`
--

DROP TABLE IF EXISTS `mausac_sp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mausac_sp` (
  `MaSP` varchar(30) NOT NULL,
  `MauSac` varchar(100) NOT NULL,
  PRIMARY KEY (`MaSP`,`MauSac`),
  CONSTRAINT `mausac_sp_ibfk_1` FOREIGN KEY (`MaSP`) REFERENCES `sanpham` (`MaSP`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mausac_sp`
--

LOCK TABLES `mausac_sp` WRITE;
/*!40000 ALTER TABLE `mausac_sp` DISABLE KEYS */;
INSERT INTO `mausac_sp` VALUES ('SP001','Đen'),('SP001','Nâu'),('SP001','Trắng'),('SP001','Xanh Dương'),('SP002','Đen'),('SP002','Nâu'),('SP002','Trắng'),('SP002','Xanh Dương'),('SP003','Đen'),('SP003','Nâu'),('SP003','Trắng'),('SP003','Xanh Dương'),('SP004','Đen'),('SP004','Đỏ'),('SP004','Nâu'),('SP004','Trắng'),('SP004','Xanh Dương');
/*!40000 ALTER TABLE `mausac_sp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nhanvien`
--

DROP TABLE IF EXISTS `nhanvien`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nhanvien` (
  `MaNV` varchar(30) NOT NULL,
  `TenNV` varchar(200) NOT NULL,
  `TenDN` varchar(100) NOT NULL,
  `MatKhau` varchar(255) NOT NULL,
  PRIMARY KEY (`MaNV`),
  UNIQUE KEY `TenDN` (`TenDN`),
  CONSTRAINT `nhanvien_chk_1` CHECK ((char_length(`MatKhau`) >= 6))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nhanvien`
--

LOCK TABLES `nhanvien` WRITE;
/*!40000 ALTER TABLE `nhanvien` DISABLE KEYS */;
INSERT INTO `nhanvien` VALUES ('B23DCCN143','Nguyễn Viết Tấn Đạt','tandat','D23CNTT'),('B23DCCN302','Ngô Đức Hiếu','ngoduchieu','D23CNTT'),('B23DCCN452','Lê Nguyễn Minh Khuê','minhkhue','D23CNTT'),('B23DCCN898','Đinh Sơn Tùng','dinhsontung','D23CNTT'),('B23DCCN926','Bùi Quang Vinh','buiquangvinh','D23CNTT'),('NV001','banhang','banhang','12345678');
/*!40000 ALTER TABLE `nhanvien` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sanpham`
--

DROP TABLE IF EXISTS `sanpham`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sanpham` (
  `MaSP` varchar(30) NOT NULL,
  `TenSP` varchar(300) NOT NULL,
  `Gia` decimal(14,2) NOT NULL,
  `MoTa` text,
  `MaTH` varchar(30) NOT NULL,
  `SoLuong` int NOT NULL,
  `NgayNhapHang` date NOT NULL DEFAULT (_utf8mb4'2025-06-09'),
  `GiamGia` int NOT NULL DEFAULT (0),
  PRIMARY KEY (`MaSP`),
  KEY `MaTH` (`MaTH`),
  CONSTRAINT `sanpham_ibfk_1` FOREIGN KEY (`MaTH`) REFERENCES `thuonghieu` (`MaTH`),
  CONSTRAINT `sanpham_chk_1` CHECK ((`Gia` > 0)),
  CONSTRAINT `sanpham_chk_2` CHECK ((`SoLuong` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sanpham`
--

LOCK TABLES `sanpham` WRITE;
/*!40000 ALTER TABLE `sanpham` DISABLE KEYS */;
INSERT INTO `sanpham` VALUES ('SP001','Nike Metcon 9 By You',4999000.00,'Đôi giày này dành cho những ai muốn khẳng định cá tính.','TH001',199,'2025-06-09',0),('SP002','Giày Streettalk',1200000.00,'Đôi giày này dành cho những ai muốn khẳng định cá tính.','TH002',166,'2025-06-09',0),('SP003','Giày Handball Special',2500000.00,'Đôi giày này dành cho những ai muốn khẳng định cá tính.','TH002',133,'2025-06-09',0),('SP004','giày đè tem',1200000.00,'alo vũ phải k em hahahaha','TH003',106,'2025-02-09',10);
/*!40000 ALTER TABLE `sanpham` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `size_sp`
--

DROP TABLE IF EXISTS `size_sp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `size_sp` (
  `MaSP` varchar(30) NOT NULL,
  `Size` varchar(20) NOT NULL,
  PRIMARY KEY (`MaSP`,`Size`),
  CONSTRAINT `size_sp_ibfk_1` FOREIGN KEY (`MaSP`) REFERENCES `sanpham` (`MaSP`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `size_sp`
--

LOCK TABLES `size_sp` WRITE;
/*!40000 ALTER TABLE `size_sp` DISABLE KEYS */;
INSERT INTO `size_sp` VALUES ('SP001','36'),('SP001','37'),('SP001','38'),('SP001','39'),('SP001','40'),('SP001','41'),('SP001','42'),('SP001','43'),('SP001','44'),('SP001','45'),('SP002','36'),('SP002','37'),('SP002','38'),('SP002','39'),('SP002','40'),('SP002','41'),('SP002','42'),('SP002','43'),('SP002','44'),('SP002','45'),('SP003','36'),('SP003','37'),('SP003','38'),('SP003','39'),('SP003','40'),('SP003','41'),('SP003','42'),('SP003','43'),('SP003','44'),('SP003','45'),('SP004','36'),('SP004','37'),('SP004','38'),('SP004','39'),('SP004','40'),('SP004','41'),('SP004','42'),('SP004','43'),('SP004','44'),('SP004','45');
/*!40000 ALTER TABLE `size_sp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sptrongdon`
--

DROP TABLE IF EXISTS `sptrongdon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sptrongdon` (
  `MaDH` varchar(30) NOT NULL,
  `MaSP` varchar(30) NOT NULL,
  `MauSac` varchar(100) NOT NULL,
  `Size` varchar(20) NOT NULL,
  `SoLuong` int NOT NULL,
  PRIMARY KEY (`MaDH`,`MaSP`,`MauSac`,`Size`),
  KEY `MaSP` (`MaSP`),
  CONSTRAINT `sptrongdon_ibfk_1` FOREIGN KEY (`MaDH`) REFERENCES `donhang` (`MaDH`),
  CONSTRAINT `sptrongdon_ibfk_2` FOREIGN KEY (`MaSP`) REFERENCES `sanpham` (`MaSP`),
  CONSTRAINT `sptrongdon_chk_1` CHECK ((`SoLuong` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sptrongdon`
--

LOCK TABLES `sptrongdon` WRITE;
/*!40000 ALTER TABLE `sptrongdon` DISABLE KEYS */;
INSERT INTO `sptrongdon` VALUES ('GH016','SP001','Xanh Dương','36',1),('GH016','SP003','Đen','42',5);
/*!40000 ALTER TABLE `sptrongdon` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `thuonghieu`
--

DROP TABLE IF EXISTS `thuonghieu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `thuonghieu` (
  `MaTH` varchar(30) NOT NULL,
  `TenTH` varchar(200) NOT NULL,
  `MoTa` text,
  PRIMARY KEY (`MaTH`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `thuonghieu`
--

LOCK TABLES `thuonghieu` WRITE;
/*!40000 ALTER TABLE `thuonghieu` DISABLE KEYS */;
INSERT INTO `thuonghieu` VALUES ('TH001','Nike','Thành lập năm 1964 tại Mỹ, Nike gắn liền với sự đổi mới trong công nghệ giày thể thao, mang đến cho khách hàng cảm giác thoải mái, bứt phá và phong cách hiện đại.'),('TH002','Adidas','Ra đời năm 1949 tại Đức, Adidas nổi tiếng toàn cầu với sự bền bỉ, hiệu năng cao, đem đến cho khách hàng trải nghiệm thể thao linh hoạt và đáng tin cậy.'),('TH003','mixi gaming',NULL),('TH004','Converse',NULL);
/*!40000 ALTER TABLE `thuonghieu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `url_sp`
--

DROP TABLE IF EXISTS `url_sp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `url_sp` (
  `MaSP` varchar(30) NOT NULL,
  `URLAnh` varchar(500) NOT NULL,
  PRIMARY KEY (`MaSP`,`URLAnh`),
  CONSTRAINT `url_sp_ibfk_1` FOREIGN KEY (`MaSP`) REFERENCES `sanpham` (`MaSP`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `url_sp`
--

LOCK TABLES `url_sp` WRITE;
/*!40000 ALTER TABLE `url_sp` DISABLE KEYS */;
INSERT INTO `url_sp` VALUES ('SP001','https://static.nike.com/a/images/t_PDP_144_v1/f_auto/1d00f231-689e-4059-b5bd-5daff661b885/custom-nike-metcon-9-shoes-by-you.png'),('SP001','https://static.nike.com/a/images/t_PDP_144_v1/f_auto/44c8ad1c-8fd1-41d2-b6ae-e86c83ccf410/custom-nike-metcon-9-shoes-by-you.png'),('SP001','https://static.nike.com/a/images/t_PDP_144_v1/f_auto/485e3a69-c1eb-4cf3-8f7e-7722b65064a8/custom-nike-metcon-9-shoes-by-you.png'),('SP002','https://assets.adidas.com/images/h_2000,f_auto,q_auto,fl_lossy,c_fill,g_auto/60fa302b89ff406fa942b8113a13554f_9366/Giay_Streettalk_trang_JP8277_03_standard.jpg'),('SP003','https://assets.adidas.com/images/e_trim:EAEEEF/c_lpad,w_iw,h_ih/b_rgb:EAEEEF/w_180,f_auto,q_auto,fl_lossy,c_fill,g_auto/08c7c0fc4ae84932864226ad74075e6e_9366/Giay_Handball_Spezial_nau_IF6490_00_plp_standard.jpg'),('SP004','https://cafefcdn.com/203337114487263232/2025/4/16/photo1641170233202-164117023330778863749311zon-1744787503868-17447875040291632568862.png'),('SP004','https://danviet-24h.ex-cdn.com/files/upload/2-2021/images/2021-06-26/42725836-adf9-4fc7-8764-9f671109ee3a-1624678195-502-width600height400.jpeg');
/*!40000 ALTER TABLE `url_sp` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-23  1:01:45
