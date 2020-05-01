import json

start = "https://maps.googleapis.com/maps/api/place/photo?key="


def load_details(city):
    with open(city+"/"+city+"_details_with_clusters.json") as f:
        return json.load(f)


def change_api(city):
    details = load_details(city)
    for place in details:
        existing = place["photo_url"]
        if "cornell" in existing:
            place["photo_url"] = "https://us.123rf.com/450wm/pavelstasevich/pavelstasevich1811/pavelstasevich181101028/112815904-stock-vector-no-image-available-icon-flat-vector-illustration.jpg?ver=6"
        else:
            new = start
            end = existing[existing.index("&"):]

            place["photo_url"] = new + \
                "AIzaSyCjWub9-U5yNbhPiqsmdaNDyzERMd828Xw" + end

    with open(city+"/"+city+"_details_with_clusters.json", 'w') as outfile:
        json.dump(details, outfile)


def main():
    change_api("new_york")
    change_api("miami")
    change_api("montreal")


if __name__ == '__main__':
    main()
