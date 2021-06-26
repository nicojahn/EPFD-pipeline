import numpy as np

codes = """HealthyGrass:1:0 208 0
StressedGrass:2:0 255 123
Artificial turf:3:96 156 49
EvergreenTrees:4:0 143 0
DeciduousTrees:5:0 76 0
BareEarth:6:47 73 146
Water:7:242 242 0
ResidentialBuildings:8:255 255 255
NonResidentialBuildings:9:216 191 216
Roads:10:0 0 255
Sidewalks:11:163 172 183
Crosswalks:12:119 104 119
MajorThoroughfares:13:0 0 167
Highways:14:0 0 79
Railways:15:16 155 229
PavedParkingLots:16:0 255 255
UnpavedParkingLots:17:0 95 173
Cars:18:193 0 193
Trains:19:244 0 0
StadiumSeats:20:223 199 180"""

def get_color_codes():
    color_codes = {int(code.split(":")[1]):{"class": code.split(":")[0], "rgb": np.asarray(code.split(":")[2].split(" "), dtype=int)[::-1]} for code in codes.split("\n")}
    return color_codes

# copied from: https://stackoverflow.com/a/59827090
def string_to_numpy(text, dtype=None):
    """
    Convert text into 1D or 2D arrays using np.matrix().
    The result is returned as an np.ndarray.
    """
    import re
    text = text.strip()
    # Using a regexp, decide whether the array is flat or not.
    # The following matches either: "[1 2 3]" or "1 2 3"
    is_flat = bool(re.match(r"^(\[[^\[].+[^\]]\]|[^\[].+[^\]])$",
                            text, flags=re.S))
    # Replace newline characters with semicolons.
    text = text.replace("]\n", "];")
    # Prepare the result.
    result = np.asarray(np.matrix(text, dtype=dtype))
    return result.flatten() if is_flat else result