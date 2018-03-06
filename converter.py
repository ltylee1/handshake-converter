import csv, os, sys

def convert_to_imp(lines, csv_name):
    templine = lines[1].split(",")
    cname = templine[0]
    orderdate = convert_date(templine[1])
    orderid = templine[2]
    ordercount = len(lines)-1
    ship_date = convert_date(get_dates(templine))
    order = ("<salorder>\n\"%s\"\n" %cname)
    order_name = "hs"+csv_name.split("order_")[1][:3]
    total_cost = 0;
    order_line = []
    for line in lines[1:]:
        line = line.split(",")
        order_line.append(parse_order(line))
        total_cost = total_cost + get_cost(line)
    order+=("\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"\n" %(ordercount, order_name, orderdate, ship_date,total_cost,"0"))
    for order_info in order_line:
        order+= order_info
    return order

def parse_order(line):
    tax_code = line[14]
    sku = line[8]
    qty = line[9]
    price = line[11]
    
    tax_type = get_tax_type(tax_code)
    tax_per = get_tax(tax_code)
    tax_amt = (float(price) * tax_per* float(qty)) 
    
    order = [sku, qty, price, str(get_cost(line)), tax_type, '0' , '1', str(tax_per*100), str(tax_amt)]
    # order = [sku, qty, price, str(get_cost(line))]
    order = "\",\"".join(order)
    return "\""+ order + "\"\n"

def get_dates(line):
    # if ship date not populated use order_date
    if line[4] == "":
        return line[1]
    else:
        return line[4]
        
def convert_date(date):
    new_date = date.split("/")
    new_date[2] = "20" + new_date[2]
    new_date = "-".join(new_date)
    return new_date
    
def get_cost(line):
    qty = int(line[9].replace("\"", ""))
    cost = float(line[11].replace("\"", ""))
    return qty*cost
    
def get_tax(code):
    if code == 'H':
        return 0.12
    elif code == "H1":
        return 0.13
    elif code == "G":
        return 0.05
    elif code == 'H2':
        return 0.15
    elif code == 'P':
        return 0.07
    elif code == 'H4':
        return 0.14
    else:
        return 0
	
def get_tax_type(code):
    if 'H' in code:
        return "HST"
    elif 'G' in code:
        return "GST"
    else:
        return "GST/HST"
    
def main(csv_name):
    
    if ('.' not in csv_name):
        csv_name = csv_name + '.csv'
    if('csv' not in csv_name):
        print "Invalid file type, please input csv file"
    
    # Open order file and read    
    hs_order = open(csv_name, 'rb')
    rows = hs_order.readlines()
    hs_order.close()
    
    
    order_content = convert_to_imp(rows, csv_name)
    # Create imp file for import and write content to it
    name = csv_name.split('.')
    with open(name[0]+".imp", 'w+') as imp:
        imp.write("<Version>\n")
        # Edit here if sage version changes
        imp.write("\"12001\", \"1\"\n")
        imp.write("</Version>\n\n")
        imp.write(order_content)
        imp.write("</salorder>\n")
    print ("Conversion complete please see %s.imp" %name[0])

try:    
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        while True:
            try:
                file_name = raw_input("Please enter filename for input: ")
                main(file_name)
            except Exception as e:
                print e
except Exception as e:
    print e