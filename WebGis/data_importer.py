import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WebGisApp.settings")
django.setup()

from WebGis.models import Bazne, Roba_s_greskom
import re
import openpyxl


path = "C:\WorkPy\WebGisApp\Bazne.xlsx"
offset = 3 #Preskačemo header

wb = openpyxl.load_workbook(path, data_only=True)
df1 = wb["Site Report"]

# cell_ids = df1["Cell ID"] gsm_ids are ints
gsm_ids = df1["L"][offset:]
cell_names = df1["B"][offset:]
ant_hs = df1["C"][offset:]
azimuths = df1["D"][offset:]
tilts = df1["G"][offset:]
lats = df1["H"][offset:]
lons = df1["I"][offset:]
beamwdths = df1["J"][offset:]
lacs = df1["K"][offset:]

Bazne.objects.all().delete()
Roba_s_greskom.objects.all().delete()

rd = {'_': ' ', '#': ' '} #replacement dict
p = re.compile("°|'")

for i in range(len(gsm_ids)):
    try:
        cell_id = str(gsm_ids[i].value)
        int(cell_id)
    except ValueError:
        cell_id = []

    cell_name = cell_names[i].value

    try:
        ant_h = float(ant_hs[i].value)
    except ValueError:
        ant_h = 20.0

    try:
        azimuth = float(azimuths[i].value)
    except ValueError:
        azimuth = float('NaN')

    try:
        tilt = float(tilts[i].value)
    except ValueError:
        tilt = []

    try:
        beamwdth = float(beamwdths[i].value)
    except ValueError:
        beamwdth = False

    try:
        lac = lacs[i].value
    except ValueError:
        lac = 0

    lat = lats[i].value
    lat_degs = re.split(p, str(lat[:-2]))
    lon = lons[i].value
    lon_degs = re.split(p, str(lon[:-2]))

    pow = 20

    uslov10 = False
    uslov11 = False
    uslov2 = False

    if len(lat_degs) > 1:
        lat_dec = str(int(lat_degs[0]) + int(lat_degs[1]) / 60 + float(lat_degs[2]) / 3600) + lat[-1]
        uslov10 = True
    else:
        lat_dec = False

    if len(lon_degs) > 1:
        lon_dec = str(int(lon_degs[0]) + int(lon_degs[1]) / 60 + float(lon_degs[2]) / 3600) + lon[-1]
        uslov11 = True
    else:
        lon_dec = False

    if (azimuth==azimuth and (beamwdth < 360)) or (not(azimuth==azimuth) and beamwdth==360.0):
        uslov2 = True
        if not (azimuth==azimuth):
            azimuth = float('Inf')
    if uslov10 and uslov11 and uslov2 and cell_id and pow:
        for old in rd:                                      #izbaciti karaktere iz naziva bazne kako je to definisano u rd
            cell_name = cell_name.replace(old, rd[old])

        bazne = Bazne(name=cell_name, cell_id=cell_id, lac=lac, height=ant_h, tilit=tilt,
              azimuth=azimuth, lat=lat_dec, lon=lon_dec, beamwdth=beamwdth, pow=pow)
        bazne.save()
    else:
        roba_sa_greskom = Roba_s_greskom(name=cell_name, cell_id=cell_id, lac=lac, height=ant_h, tilit=tilt,
              azimuth=azimuth, lat=lat_dec, lon=lon_dec, beamwdth=beamwdth, pow=pow)
        roba_sa_greskom.save()
