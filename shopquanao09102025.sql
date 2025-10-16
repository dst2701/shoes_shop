CREATE DATABASE  IF NOT EXISTS `shopgiaydep09102025` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `shopgiaydep09102025`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: shopgiaydep09102025
-- ------------------------------------------------------
-- Server version	8.0.37

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
  CONSTRAINT `cthoadon_ibfk_2` FOREIGN KEY (`MaSP`) REFERENCES `sanpham` (`MaSP`),
  CONSTRAINT `cthoadon_chk_1` CHECK ((`SoLuongMua` >= 0)),
  CONSTRAINT `cthoadon_chk_2` CHECK ((`DonGia` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cthoadon`
--

LOCK TABLES `cthoadon` WRITE;
/*!40000 ALTER TABLE `cthoadon` DISABLE KEYS */;
INSERT INTO `cthoadon` VALUES ('HD001','SP001','Nike Metcon 9 By You','Đen','41',1,4999000.00,4999000.00),('HD001','SP002','Giày Streettalk','Trắng','42',2,1200000.00,2400000.00),('HD002','SP003','Giày Handball Spezial','Nâu','40',1,2500000.00,2500000.00),('HD003','SP001','Nike Metcon 9 By You','Trắng','42',1,4999000.00,4999000.00),('HD003','SP002','Giày Streettalk','Trắng','43',3,1200000.00,3600000.00),('HD003','SP003','Giày Handball Spezial','Nâu','41',2,2500000.00,5000000.00),('HD004','SP001','Nike Metcon 9 By You','Xanh dương','43',1,4999000.00,4999000.00),('HD005','SP002','Giày Streettalk','Trắng','44',1,1200000.00,1200000.00),('HD005','SP003','Giày Handball Spezial','Nâu','40',2,2500000.00,5000000.00),('HD006','SP002','Giày Streettalk','Trắng','42',2,1200000.00,2400000.00),('HD007','SP001','Nike Metcon 9 By You','Xanh dương','41',1,4999000.00,4999000.00),('HD007','SP003','Giày Handball Spezial','Nâu','40',2,2500000.00,5000000.00),('HD008','SP001','Nike Metcon 9 By You','Đen','42',1,4999000.00,4999000.00),('HD009','SP002','Giày Streettalk','Trắng','43',2,1200000.00,2400000.00),('HD009','SP003','Giày Handball Spezial','Nâu','39',1,2500000.00,2500000.00),('HD010','SP001','Nike Metcon 9 By You','Trắng','44',1,4999000.00,4999000.00),('HD010','SP002','Giày Streettalk','Trắng','42',1,1200000.00,1200000.00),('HD010','SP003','Giày Handball Spezial','Nâu','41',2,2500000.00,5000000.00);
/*!40000 ALTER TABLE `cthoadon` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `giohang`
--

DROP TABLE IF EXISTS `giohang`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `giohang` (
  `MaGH` varchar(30) NOT NULL,
  `MaKH` varchar(30) NOT NULL,
  PRIMARY KEY (`MaGH`),
  UNIQUE KEY `MaKH` (`MaKH`),
  CONSTRAINT `giohang_ibfk_1` FOREIGN KEY (`MaKH`) REFERENCES `khachhang` (`MaKH`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `giohang`
--

LOCK TABLES `giohang` WRITE;
/*!40000 ALTER TABLE `giohang` DISABLE KEYS */;
INSERT INTO `giohang` VALUES ('GH001','KH001'),('GH002','KH002'),('GH003','KH003'),('GH004','KH004'),('GH005','KH005'),('GH006','KH006'),('GH007','KH007'),('GH008','KH008'),('GH009','KH009'),('GH010','KH010');
/*!40000 ALTER TABLE `giohang` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `giohangchuasanpham`
--

DROP TABLE IF EXISTS `giohangchuasanpham`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `giohangchuasanpham` (
  `MaGH` varchar(30) NOT NULL,
  `MaSP` varchar(30) NOT NULL,
  `MauSac` varchar(100) NOT NULL,
  `Size` varchar(20) NOT NULL,
  `SoLuong` int NOT NULL,
  PRIMARY KEY (`MaGH`,`MaSP`,`MauSac`,`Size`),
  KEY `MaSP` (`MaSP`),
  CONSTRAINT `giohangchuasanpham_ibfk_1` FOREIGN KEY (`MaGH`) REFERENCES `giohang` (`MaGH`),
  CONSTRAINT `giohangchuasanpham_ibfk_2` FOREIGN KEY (`MaSP`) REFERENCES `sanpham` (`MaSP`),
  CONSTRAINT `giohangchuasanpham_chk_1` CHECK ((`SoLuong` > 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `giohangchuasanpham`
--

LOCK TABLES `giohangchuasanpham` WRITE;
/*!40000 ALTER TABLE `giohangchuasanpham` DISABLE KEYS */;
INSERT INTO `giohangchuasanpham` VALUES ('GH001','SP001','Đen','41',1),('GH001','SP002','Trắng','42',2),('GH002','SP003','Nâu','40',1),('GH003','SP001','Trắng','42',1),('GH003','SP002','Trắng','43',3),('GH003','SP003','Nâu','41',2),('GH004','SP001','Xanh dương','43',1),('GH005','SP002','Trắng','44',1),('GH005','SP003','Nâu','40',2),('GH006','SP002','Trắng','42',2),('GH007','SP001','Xanh dương','41',1),('GH007','SP003','Nâu','40',2),('GH008','SP001','Đen','42',1),('GH009','SP002','Trắng','43',2),('GH009','SP003','Nâu','39',1),('GH010','SP001','Trắng','44',1),('GH010','SP002','Trắng','42',1),('GH010','SP003','Nâu','41',2);
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
  `NgayLap` date NOT NULL,
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
INSERT INTO `hoadon` VALUES ('HD001','KH001','B23DCCN143','2025-10-09'),('HD002','KH002','B23DCCN302','2025-10-09'),('HD003','KH003','B23DCCN452','2025-10-09'),('HD004','KH004','B23DCCN898','2025-10-09'),('HD005','KH005','B23DCCN926','2025-10-09'),('HD006','KH006','B23DCCN143','2025-10-09'),('HD007','KH007','B23DCCN302','2025-10-09'),('HD008','KH008','B23DCCN452','2025-10-09'),('HD009','KH009','B23DCCN898','2025-10-09'),('HD010','KH010','B23DCCN926','2025-10-09');
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
INSERT INTO `khachhang` VALUES ('KH001','Nguyễn Văn Bảo','0912345678','Bảo Nhai - Lào Cai','nguyenvanbao','abc123'),('KH002','Vũ Minh Dương','0987654321','Vũ Dương - Ninh Bình','vuminhduong','87654321'),('KH003','Trần Quang Hà','0901122334','Hà Đông - Hà Nội','tranquangha','1234567'),('KH004','Phạm Thị Hòa','0933445566','Yên Hòa - Hà Nội','phamthihoa','hoamai89'),('KH005','Đỗ Văn Nghĩa','0977223344','Yên Nghĩa - Hà Nội','dovannghia','nghia1234'),('KH006','Lê Thị Minh','0922334455','Tân Minh - Hải Phòng','lethiminh','minh567'),('KH007','Hoàng Anh Tuấn','0966889900','Bảo Thắng - Lào Cai','hoanganhtuan','tuantuan'),('KH008','Nguyễn Thị Lan','0944556677','Bắc Hà - Lào Cai','nguyenthilan','lan9999'),('KH009','Bùi Văn Hùng','09119992233','Hà Đông - Hà Nội','buivanhung','hung12345'),('KH010','Trần Thị Mai','0988112233','Vũ Dương - Ninh Bình','tranthimai','maimandinh');
/*!40000 ALTER TABLE `khachhang` ENABLE KEYS */;
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
INSERT INTO `nhanvien` VALUES ('B23DCCN143','Nguyễn Viết Tấn Đạt','tandat','D23CNTT'),('B23DCCN302','Ngô Đức Hiếu','ngoduchieu','D23CNTT'),('B23DCCN452','Lê Nguyễn Minh Khuê','minhkhue','D23CNTT'),('B23DCCN898','Đinh Sơn Tùng','dinhsontung','D23CNTT'),('B23DCCN926','Bùi Quang Vinh','buiquangvinh','D23CNTT');
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
INSERT INTO `sanpham` VALUES ('SP001','Nike Metcon 9 By You',4999000.00,'Đôi giày này dành cho những ai muốn khẳng định cá tính.','TH001',10),('SP002','Giày Streettalk',1200000.00,'Đôi giày này dành cho những ai muốn khẳng định cá tính.','TH002',20),('SP003','Giày Handball Spezial',2500000.00,'Đôi giày này dành cho những ai muốn khẳng định cá tính.','TH002',30);
/*!40000 ALTER TABLE `sanpham` ENABLE KEYS */;
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
INSERT INTO `thuonghieu` VALUES ('TH001','Nike','Thành lập năm 1964 tại Mỹ, Nike gắn liền với sự đổi mới trong công nghệ giày thể thao, mang đến cho khách hàng cảm giác thoải mái, bứt phá và phong cách hiện đại.'),('TH002','Adidas','Ra đời năm 1949 tại Đức, Adidas nổi tiếng toàn cầu với sự bền bỉ, hiệu năng cao, đem đến cho khách hàng trải nghiệm thể thao linh hoạt và đáng tin cậy.');
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
INSERT INTO `url_sp` VALUES ('SP001','https://static.nike.com/a/images/t_PDP_144_v1/f_auto/1d00f231-689e-4059-b5bd-5daff661b885/custom-nike-metcon-9-shoes-by-you.png'),('SP001','https://static.nike.com/a/images/t_PDP_144_v1/f_auto/44c8ad1c-8fd1-41d2-b6ae-e86c83ccf410/custom-nike-metcon-9-shoes-by-you.png'),('SP001','https://static.nike.com/a/images/t_PDP_144_v1/f_auto/485e3a69-c1eb-4cf3-8f7e-7722b65064a8/custom-nike-metcon-9-shoes-by-you.png'),('SP002','https://assets.adidas.com/images/h_2000,f_auto,q_auto,fl_lossy,c_fill,g_auto/60fa302b89ff406fa942b8113a13554f_9366/Giay_Streettalk_trang_JP8277_03_standard.jpg'),('SP003','https://assets.adidas.com/images/e_trim:EAEEEF/c_lpad,w_iw,h_ih/b_rgb:EAEEEF/w_180,f_auto,q_auto,fl_lossy,c_fill,g_auto/08c7c0fc4ae84932864226ad74075e6e_9366/Giay_Handball_Spezial_nau_IF6490_00_plp_standard.jpg');
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

-- Dump completed on 2025-10-09 12:46:29
