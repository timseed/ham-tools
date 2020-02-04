#
#
#
# def beacon_tests():
#     """
#     Beacons testing
#     """
#
#     dx = beacons(ScreenOutput=True)
#     dx.SetBand(14)
#     dx.beacon_start(timeout=50)
#     dx.dump_band(4)
#     junk = 1
#
#
# def dxspider_tests():
#     host = "gb7mbc.spoo.org"
#     port = 8000
#     call = "a45wg"
#     dxs = dxspider(host, port, call)
#     if dxs.do_connect():
#         for i in range(2000):
#             dxs.get_dx()
#
#
# def rbn_tests():
#     r = Rbn()
#     r.loop()
#
#
# # dxcc_tests()
# # adif_tests()
# # beacon_tests()
# # dxspider_tests()
# rbn_tests()
#
# print("Finished Tests")
