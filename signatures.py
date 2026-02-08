import json, re

data_path = "time_signatures.json"
with open(data_path, "r") as file:
    data = json.load(file)

def _collapse_sig_lists(s): # Make "sig": [4,4] not indent because it is ugly
    return re.sub(
        r'\[\s*(\d+),\s*(\d+)\s*\]',
        r'[\1, \2]',
        s
    )

def new(name:str, signatures:dict, bpm:float, locked:bool=False, dontAppend:bool=False):
    """
        Create a new signature dict
        
        Parameters:
            name (str): Name of the song for the time signature
            bpm (float): Beats Per Minute 
            locked (bool): Prevent deletion via `delete(name)`
            signatures (dict): Signatures in the song:
                'sig' (list): The time signature,
                'amount' (int): The amount of measures to repeat for
                
                Should look like: 
                [
                    {'sig':[0,0], 'amount':0}
                ]
                Example:
                [
                    {'sig':  [4, 4], 'amount': 8},
                    {'sig':  [4, 8], 'amount': 4}
                ]
    """

    doesExist = get(name)[1]
    
    if doesExist:
        print(f"\"{name}\" already exists")
        return f"\"{name}\" already exists"

    newDict = {
        "name": name,
        "bpm": bpm,
        "locked": locked,
        "time_signatures": signatures,
    }
    
    data.append(newDict)
    if not dontAppend:
        with open(data_path, "w") as file:
            json_str = json.dumps(data, indent=4)
            json_str = _collapse_sig_lists(json_str)
            file.write(json_str)
        return data
    else:
        return data

def delete(name: str):
    popped = None
    for num, i in enumerate(data):
        if i["name"].lower() == name.lower():
            if i["locked"] == True:
                return None
            
            popped = data.pop(num)
            with open(data_path, "w") as file:
                json_str = json.dumps(data, indent=4)
                json_str = _collapse_sig_lists(json_str)
                file.write(json_str)
                
            break
    return popped

def lock(name: str, locked:bool=True):
    for num, i in enumerate(data):
        if i["name"].lower() == name.lower():
            data[num]["locked"] = locked
            
            with open(data_path, "w") as file:
                json_str = json.dumps(data, indent=4)
                json_str = _collapse_sig_lists(json_str)
                file.write(json_str)
                
            break

def get(name:str, dataType:str="signatures"):
    dataType = dataType.lower()
    try:
        for i in data:
            if i["name"].lower() == name.lower():
                if (dataType == "signatures") or (dataType == "signature"):
                    signatures = []
                    for j in i["time_signatures"]:
                        for amount in range(j["amount"]):
                            signatures.append((j["sig"][0], j["sig"][1])) # turn list into tuple then append
                elif dataType == "bpm":
                    return i["bpm"], True
                else:
                    ValueError("Must be 'signatures' or 'bpm'")
        
        return signatures, True
    
    except Exception as e:
        return e, False