from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
from waitress import serve
from train import Model
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Checks if a request is valid by ensuring that the required keys exist.


def isValidRequest(keys, payload):
    for key in keys:
        if key not in payload:
            return False
    return True


@app.route('/train', methods=['POST'])
@cross_origin()
# This endpoint recieves training data, saves and trains the model.
def trainNew():
    print("request: train")
    # TODO: validate request
    payload = request.json
    # name of model, whether you are re-training the model, data to train the model
    keys = ["modelName", "isNewModel", "data"]
    if not isValidRequest(keys, payload):
        return {"status": 400, "error": "Invalid request"}
    modelName = payload["modelName"]
    data = None
    try:
        data = Model.parseData(payload["data"])
    except Exception as e:
        return {"status": 400, "error": "Invalid data format: " + str(e)}
    # Test training data, can be removed.
    # data = [('59577231369015 $1412.00 MEMBER $1199.00 Lenovo IdeaCentre Gaming5 17IAB7 90T100AJST - i5-12400F / 8GB RAM / 512GB SSD+1TB HDD / NVIDIA GTX1650', {'entities': [(40, 142, 'PRODUCT'), (15, 23, 'PRICE'), (24, 39, 'MEMBER'), (0, 14, 'UPC')]}),
    #         ('Arlo Ultra 2 Spotlight Camera – 4K UHD & HDR – 2 camera system (VMS5240-200APS) MEMBER $769.00 $1199.00 1126167890555',
    #          {'entities': [(0, 79, 'PRODUCT'), (95, 103, 'PRICE'), (80, 94, 'MEMBER'), (104, 117, 'UPC')]}),
    #         ('MEMBER $849.00 $999.00 55199180869015 Google Pixel 7 Obsidian 8+128GB 5G (GA03923-US)',
    #          {'entities': [(38, 85, 'PRODUCT'), (15, 22, 'PRICE'), (0, 14, 'MEMBER'), (23, 37, 'UPC')]}),
    #         ('MEMBER $230.00 Fitbit Charge 5 Fitness Tracker (Lunar White, Soft Gold Stainless Steel) 55194980199015 $238.00', {
    #          'entities': [(15, 87, 'PRODUCT'), (103, 110, 'PRICE'), (0, 14, 'MEMBER'), (88, 102, 'UPC')]}),
    #         ('$199.00 5519097199015 MEMBER $139.30 Elecom DST-C01SV Type-C Docking station/PD/Tpye-C/3 x USB',
    #          {'entities': [(37, 94, 'PRODUCT'), (0, 7, 'PRICE'), (22, 36, 'MEMBER'), (8, 21, 'UPC')]}),
    #         ('$309.00 MEMBER $229.00 Canon G3020 Ink Efficient Wireless All-In-One Printer 5515697899015',
    #          {'entities': [(23, 76, 'PRODUCT'), (0, 7, 'PRICE'), (8, 22, 'MEMBER'), (77, 90, 'UPC')]}),
    #         ('Baseus CAHUB-L0G thunderbolt C+Pro smart HUB docking station (Grey) 5169167890555 $89.90 MEMBER $80.91',
    #          {'entities': [(0, 67, 'PRODUCT'), (82, 88, 'PRICE'), (89, 102, 'MEMBER'), (68, 81, 'UPC')]}),
    #         ('$489 Seagate One Touch SSD 2TB (Silver) MEMBER $289.00 13171118719815', {
    #             'entities': [(5, 39, 'PRODUCT'), (0, 4, 'PRICE'), (40, 54, 'MEMBER'), (55, 69, 'UPC')]}),
    #         ('$32.00 5519097899015 D-Link DGS-105 5-Port Gigabit Unmanaged Desktop Switch (Metal) MEMBER $29.00',
    #          {'entities': [(21, 83, 'PRODUCT'), (0, 6, 'PRICE'), (84, 97, 'MEMBER'), (7, 20, 'UPC')]}),
    #         ('Apple Iphone 13 Pro $1500.00 19812324121 MEMBER $1400.00', {'entities': [
    #             (0, 19, 'PRODUCT'), (20, 28, 'PRICE'), (41, 56, 'MEMBER'), (29, 40, 'UPC')]}),
    #         ('MEMBER $2298.00 55139991369015 $2926.00 HP OMEN 16-n0012AX 6G248PA - R7-6800H, 32GB RAM, 1TB SSD, RTX3060 ',
    #          {'entities': [(40, 105, 'PRODUCT'), (31, 39, 'PRICE'), (0, 15, 'MEMBER'), (16, 30, 'UPC')]}),
    #         ('$339.00 Philips Hue Lightstrip Outdoor [5M] MEMBER $322.05 55996410719815', {
    #             'entities': [(8, 43, 'PRODUCT'), (0, 7, 'PRICE'), (44, 58, 'MEMBER'), (59, 73, 'UPC')]}),
    #         ('Samsung Galaxy A30 $448.00 MEMBER $100.00 12344124231', {'entities': [
    #             (0, 18, 'PRODUCT'), (19, 26, 'PRICE'), (27, 41, 'MEMBER'), (42, 53, 'UPC')]}),
    #         ('Apple Iphone 10 $1100.00 MEMBER $1000.00 19844124121', {'entities': [
    #             (0, 15, 'PRODUCT'), (16, 24, 'PRICE'), (25, 40, 'MEMBER'), (41, 52, 'UPC')]}),
    #         ('Asus ROG Zephyrus Duo SE 15 (GX551QR-HF087T R9 5980HX, 32GB RAM, 1TB SSD, RTX3070, 300HZ) (Off Black) MEMBER $4198.00 1169167890555 $5898.00',
    #          {'entities': [(0, 101, 'PRODUCT'), (132, 140, 'PRICE'), (102, 117, 'MEMBER'), (118, 131, 'UPC')]}),
    #         ('55139413513115 MEMBER $49.00 $59.00 Logitech K380 Multi-Device Bluetooth Keyboard (Blue)  Fulfilled By: Challenger',
    #          {'entities': [(36, 88, 'PRODUCT'), (29, 35, 'PRICE'), (15, 28, 'MEMBER'), (0, 14, 'UPC')]}),
    #         ('Belkin BSV804sa2M 8-Outlets Surge Protection Strip with 2 USB Ports 5165167890555 MEMBER $79.00 $100.00',
    #          {'entities': [(0, 67, 'PRODUCT'), (96, 103, 'PRICE'), (82, 95, 'MEMBER'), (68, 81, 'UPC')]}),
    #         ('55990133513115 MSI Cyborg 15 A12VF - i7-12650H, 16GB RAM, 512GB SSD, RTX4060, 15.6-inch $2299.00 MEMBER $1999.00',
    #          {'entities': [(15, 87, 'PRODUCT'), (88, 96, 'PRICE'), (97, 112, 'MEMBER'), (0, 14, 'UPC')]}),
    #         ('Microsoft Surface Pro 9 QIX-00030 512GB i7 16GB Graphite $2278.00 31248513137 MEMBER $2000.00',
    #          {'entities': [(0, 56, 'PRODUCT'), (57, 65, 'PRICE'), (78, 93, 'MEMBER'), (66, 77, 'UPC')]}),
    #         ('Marshall Mode Earphones with Mic (Black & White) 55135133513115 MEMBER $93.00 $99.00', {
    #             'entities': [(0, 48, 'PRODUCT'), (78, 84, 'PRICE'), (64, 77, 'MEMBER'), (49, 63, 'UPC')]}),
    #         ('SanDisk Ultra microSDXC UHS-I 128GB A1 U1 C10 120MB/s [SDSQUA4-128G-GN6MN] 13178498719815 $32.00 MEMBER $31.00', {
    #             'entities': [(0, 74, 'PRODUCT'), (90, 96, 'PRICE'), (97, 110, 'MEMBER'), (75, 89, 'UPC')]}),
    #         ('Fitbit Aria Air FB203WT Weighing Scale (White) $78.00 MEMBER $58.00 31581512137', {
    #             'entities': [(0, 46, 'PRODUCT'), (47, 53, 'PRICE'), (54, 67, 'MEMBER'), (68, 79, 'UPC')]}),
    #         ('55139624569015 Jabra Speak 710 UC Speakerphone (7710-509) MEMBER $516.00 $536.00',
    #          {'entities': [(15, 57, 'PRODUCT'), (73, 80, 'PRICE'), (58, 72, 'MEMBER'), (0, 14, 'UPC')]}),
    #         ('$239.00 Shokz OpenSwim Bone Conduction Open-Ear MP3 Swimming Headphones (Black) MEMBER $230.00 13172018719815',
    #          {'entities': [(8, 79, 'PRODUCT'), (0, 7, 'PRICE'), (80, 94, 'MEMBER'), (95, 109, 'UPC')]}),
    #         ('Samsung Galaxy S23 Ultra [Green] 12+512GB 5G $2098.00 MEMBER $1748.00 13996498719815', {
    #             'entities': [(0, 44, 'PRODUCT'), (45, 53, 'PRICE'), (54, 69, 'MEMBER'), (70, 84, 'UPC')]}),
    #         ('55139915135615 MEMBER $569.00 Linksys MX8400 Velop Tri-Band AX4200 Whole Home Mesh WiFi 6 System (2 Pack) Works with Apple HomeKit $799.00',
    #          {'entities': [(30, 130, 'PRODUCT'), (131, 138, 'PRICE'), (15, 29, 'MEMBER'), (0, 14, 'UPC')]}),
    #         ('19812324121 Google pixel 5A $1500.00 MEMBER $1400.00', {'entities': [
    #             (12, 27, 'PRODUCT'), (28, 36, 'PRICE'), (37, 52, 'MEMBER'), (0, 11, 'UPC')]}),
    #         ('55134145541611 $275.00 JBL Quantum Duo PC Gaming Speaker MEMBER $179.00', {
    #             'entities': [(23, 56, 'PRODUCT'), (15, 22, 'PRICE'), (57, 71, 'MEMBER'), (0, 14, 'UPC')]}),
    #         ('Sony speaker $1200.00 MEMBER $1100.00 19832124121', {'entities': [
    #             (0, 12, 'PRODUCT'), (13, 21, 'PRICE'), (22, 37, 'MEMBER'), (38, 49, 'UPC')]}),
    #         ('MEMBER $58.41 $64.90 Omars OMWS008 10000mAh Magnetic Wireless Charging Power Bank 55996410713115', {
    #             'entities': [(21, 81, 'PRODUCT'), (14, 20, 'PRICE'), (0, 13, 'MEMBER'), (82, 96, 'UPC')]}),
    #         ('Playstation VR2 Horizon Call of the Mountain Bundle ASIA-00446 09809138719815 MEMBER $939.00 $1000.00',
    #          {'entities': [(0, 62, 'PRODUCT'), (93, 101, 'PRICE'), (78, 92, 'MEMBER'), (63, 77, 'UPC')]}),
    #         ('$599.00 Bose Noise Cancelling Headphones 700 (Black) MEMBER $576.00 5515167890555', {
    #             'entities': [(8, 52, 'PRODUCT'), (0, 7, 'PRICE'), (53, 67, 'MEMBER'), (68, 81, 'UPC')]}),
    #         ('55139991369015 Huawei MatePad SE 10.36" Black 4+128GB Wifi (HW-AGASSI5-W09) $300.00 MEMBER $298.00',
    #          {'entities': [(15, 75, 'PRODUCT'), (76, 83, 'PRICE'), (84, 98, 'MEMBER'), (0, 14, 'UPC')]}),
    #         ('MEMBER $89.91 55194991369015 Hoco S31 Wireless Microphone (Mic+Receiver for Type-C) $99.90',
    #          {'entities': [(29, 83, 'PRODUCT'), (84, 90, 'PRICE'), (0, 13, 'MEMBER'), (14, 28, 'UPC')]}),
    #         ('Microsoft Surface Pro 9 QIX-00030 512GB i7 16GB Graphite 31248513137 $2278.00 MEMBER $2000.00',
    #          {'entities': [(0, 56, 'PRODUCT'), (69, 77, 'PRICE'), (78, 93, 'MEMBER'), (57, 68, 'UPC')]}),
    #         ('Netgear AC1200 WiFi Range Extender (EX6120-100UKS) 55990180713115 $99.00 MEMBER $69.00',
    #          {'entities': [(0, 50, 'PRODUCT'), (66, 72, 'PRICE'), (73, 86, 'MEMBER'), (51, 65, 'UPC')]}),
    #         ('MEMBER $20.00 TP-LINK 150Mbps High Gain Wireless USB Adapter (TL-WN722N) $19.00 09809999719815',
    #          {'entities': [(14, 72, 'PRODUCT'), (73, 79, 'PRICE'), (0, 13, 'MEMBER'), (80, 94, 'UPC')]}),
    #         ('MEMBER $148.00 Epson WF-2851 All-in-One Inkjet Printer $158.00 55194127199015',
    #          {'entities': [(15, 54, 'PRODUCT'), (55, 62, 'PRICE'), (0, 14, 'MEMBER'), (63, 77, 'UPC')]}),
    #         ('Valore Nylon Braided Lightning Cable (MA52) MEMBER $19.90 $26.90 09809173719815', {
    #             'entities': [(0, 43, 'PRODUCT'), (58, 64, 'PRICE'), (44, 57, 'MEMBER'), (65, 79, 'UPC')]}),
    #         ('$154.90 Razer Barracuda X (2021) Wireless Gaming Headset (Black) MEMBER $149.00 55996498719815', {
    #             'entities': [(8, 64, 'PRODUCT'), (0, 7, 'PRICE'), (65, 79, 'MEMBER'), (80, 94, 'UPC')]}),
    #         ('$31.00 Braun Ear & Nose trimmer (EN10) 5515167890015 MEMBER $29.00', {'entities': [
    #             (7, 38, 'PRODUCT'), (0, 6, 'PRICE'), (53, 66, 'MEMBER'), (39, 52, 'UPC')]}),
    #         ('MEMBER $507.00 $529.00 Garmin Forerunner 245 Music Running Watch (Black) 55194980869015', {
    #             'entities': [(23, 72, 'PRODUCT'), (15, 22, 'PRICE'), (0, 14, 'MEMBER'), (73, 87, 'UPC')]}),
    #         ('Valore Rechargeable Electric Mosquito Swatter (AC94) 31248582137 $2071.50 MEMBER $1700.00', {
    #             'entities': [(0, 52, 'PRODUCT'), (65, 73, 'PRICE'), (74, 89, 'MEMBER'), (53, 64, 'UPC')]}),
    #         ('Microsoft Surface Laptop Studio (1TB, i7, 32GB RAM) [ABY-00017] 55914133513115 $4100.00 MEMBER $4029.00', {
    #             'entities': [(0, 63, 'PRODUCT'), (79, 87, 'PRICE'), (88, 103, 'MEMBER'), (64, 78, 'UPC')]}),
    #         ('$40.00 MEMBER $37.20 Brother PT-H107B Labeller Machine 5515697890015',
    #          {'entities': [(21, 54, 'PRODUCT'), (0, 6, 'PRICE'), (7, 20, 'MEMBER'), (55, 68, 'UPC')]}),
    #         ('MacBook Pro 13-inch Space Grey M2 with 8-core CPU and 10-core GPU, 8GB RAM, 256GB SSD [MNEH3ZP/A] $1900.00 1124567890555 MEMBER $1896.00', {
    #             'entities': [(0, 97, 'PRODUCT'), (98, 106, 'PRICE'), (107, 120, 'UPC'), (121, 136, 'MEMBER')]}),
    #         ('31238512137 Netgear Orbi RBK853 AX6000 Whole Home Tri-Band Mesh Wifi $1399.00 MEMBER $1000.00',
    #          {'entities': [(12, 68, 'PRODUCT'), (69, 77, 'PRICE'), (78, 93, 'MEMBER'), (0, 11, 'UPC')]}),
    #         ('[Demo Set] XAsus Vivobook Flip 14 TP470EA-EC335W - i5-1135G7, 16GB, 512GB, W11, 14-inch (Black) $1498.00 MEMBER $1168.00 1234567890555',
    #          {'entities': [(0, 95, 'PRODUCT'), (96, 104, 'PRICE'), (105, 120, 'MEMBER'), (121, 134, 'UPC')]}),
    #         ('OPPO Reno7 Z [Cosmic Black] 8+128GB 5G 55981110713115 $399.00 MEMBER $379.00', {
    #             'entities': [(0, 38, 'PRODUCT'), (54, 61, 'PRICE'), (62, 76, 'MEMBER'), (39, 53, 'UPC')]}),
    #         ('09872018719815 $1699.00 Sonos Arc Smart Soundbar (Black) MEMBER $1656.00', {
    #             'entities': [(24, 56, 'PRODUCT'), (15, 23, 'PRICE'), (57, 72, 'MEMBER'), (0, 14, 'UPC')]}),
    #         ('MEMBER $1700.00 31248582137 $300179.00 Verbatim DVD-R 16X 50pcs IJP -43533',
    #          {'entities': [(39, 74, 'PRODUCT'), (28, 38, 'PRICE'), (0, 15, 'MEMBER'), (16, 27, 'UPC')]})
    #         ]
    isNewModel = payload["isNewModel"]

    TrainObject = Model()

    return TrainObject.train(modelName, data, isNewModel)

# send over test parameters -> return output genereated by previously created model, else return error
# Need to check that number of inputs === number of inputs model requires


@app.route('/test', methods=['POST'])
@cross_origin()
# This endpoint allows users to tests models that they have previously trained
def test():
    print("request: test")
    payload = request.json
    # name of model to test, array of strings to test model
    keys = ["modelName", "testArray"]
    if not isValidRequest(keys, payload):
        return {"status": 400, "error": "Invalid request"}
    modelName = payload["modelName"]
    testString = payload["testArray"]
    TrainObject = Model()

    return TrainObject.test(modelName, testString)

if __name__ == "__main__":
    print("Running server")
    # Change values here for server address
    serve(app, host="localhost", port=5000)
