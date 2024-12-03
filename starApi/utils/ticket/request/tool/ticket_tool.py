def get_seat_type(seats):
    for seat in seats:
        return seat.get('id')


def cookie_to_dict(response):
    cookie_object = {}
    filter_key = ['path', 'max-age', 'expires']
    item = response.headers.get('set-cookie') or response.headers.get('Set-Cookie')
    if item:
        item = item.replace(',', ';')
        item = item.split(';')
        for query in item:
            query_obj = query.strip().split('=')
            if isinstance(query_obj, list) and len(query_obj) == 2:
                name, value = query_obj
                if value == '""':
                    continue
                if name.lower() not in filter_key:
                    cookie_object.update({name: value})
    return cookie_object


def request_set_cookie(response, get_cookie, expires):
    if get_cookie:
        for k, v in get_cookie.items():
            response.set_cookie(key=k, value=v, expires=expires, secure=False, httponly=True)
    return response


def make_order_data(item):
    TicketList = []
    oldPassengerList = []
    tour_flag = ''
    for kwargs in item:
        id_no = kwargs.get("id_no")
        mobile_no = kwargs.get("mobile_no") or ""
        allEncStr = kwargs.get("allEncStr") or ""
        id_type = kwargs.get("id_type")
        name = kwargs.get("name")
        seat_type = kwargs.get("seat_type")
        ticket_type = kwargs.get("ticket_type")
        tour_flag = kwargs.get("tour_flag")
        TicketStr = f"{seat_type},0,{ticket_type},{name},{id_type},{id_no},{mobile_no},N,{allEncStr}"
        TicketList.append(TicketStr)

        oldPassengerStr = f"{name},1,{id_no},1"
        oldPassengerList.append(oldPassengerStr)
    TicketStr = '_'.join(TicketList)
    oldPassengerStr = '_'.join(oldPassengerList)
    return {"TicketStr": TicketStr, "oldStr": oldPassengerStr, "tour_flag": tour_flag}


def comfirm_order_data(item):
    TicketList = []
    oldPassengerList = []
    tour_flag = ''
    purpose_codes = ''
    leftTicketStr = ''
    train_location = ''
    key_check = ''
    for kwargs in item:
        id_no = kwargs.get("id_no")
        mobile_no = kwargs.get("mobile_no") or ""
        allEncStr = kwargs.get("allEncStr") or ""
        id_type = kwargs.get("id_type")
        name = kwargs.get("name")
        seat_type = kwargs.get("seat_type")
        ticket_type = kwargs.get("ticket_type")
        train_location = kwargs.get("train_location")
        purpose_codes = kwargs.get("purpose_codes")
        leftTicketStr = kwargs.get("leftTicketStr")
        key_check = kwargs.get("key_check")

        TicketStr = f"{seat_type},0,{ticket_type},{name},{id_type},{id_no},{mobile_no},N,{allEncStr}"
        TicketList.append(TicketStr)

        oldPassengerStr = f"{name},1,{id_no},1"
        oldPassengerList.append(oldPassengerStr)
    TicketStr = '_'.join(TicketList)
    oldPassengerStr = '_'.join(oldPassengerList)
    return {"TicketStr": TicketStr, "oldStr": oldPassengerStr, "tour_flag": tour_flag, 'purpose_codes': purpose_codes,
            "leftTicketStr": leftTicketStr, "train_location": train_location, "key_check": key_check}