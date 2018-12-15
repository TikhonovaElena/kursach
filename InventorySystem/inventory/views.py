from django.shortcuts import render
import sys, string, os, json
from .models import Post

log_info = {"login": "root", "password": "root"}

def open_file(name):
	file = r"/inventory/{0}.json".format(name)
	path = os.getcwd() + file
	with open(path, "r", encoding="utf-8") as fh:
		data = json.load(fh)
	return data


def write_in_file(name, text):
	file = r"/inventory/{0}.json".format(name)
	path = os.getcwd() + file
	with open(path, "w", encoding="utf-8") as fh:
		fh.write(text)


def org_list(request):
	orgs = open_file("Organizations")
	return render(request, "inventory/org_list.html", {"orgs": orgs})


def org_info(request):
	orgs = open_file("Organizations")
	a = request.POST.get("org_name")
	print(a)
	for org in orgs:
		if org["org_name"] == request.POST.get("org_name"):
			return render(request, "inventory/org_info.html", {"org": org})
	return render(request, "inventory/org_list.html", {"orgs": orgs})


def wealth_info(request):
    print(request.POST.get("name"), request.POST.get("org_name"))
    orgs = open_file("Organizations")
    for org in orgs:
        if org["org_name"] == request.POST.get("org_name"):
            for w in org["wealth"]:
                if w["name"] == request.POST.get("name"):
                    return render(request, "inventory/wealth_info.html", {'w': w})


def add_org(request):
	orgs = open_file("Organizations")
	new_org = {
		"org_name": request.POST.get("org_name"),
		"create_date": request.POST.get("create_date"),
		"address": request.POST.get("address"),
		"org_description": request.POST.get("org_description"),
		"director_first_name": request.POST.get("director_first_name"),
		"director_last_name": request.POST.get("director_last_name"),
		"director_middle_name": request.POST.get("director_middle_name"),
		"director_DOB": request.POST.get("director_DOB"),
		"wealth": []
	}
	normalno = True
	for org in orgs:
		if org["org_name"] == new_org["org_name"] or new_org["org_name"] == "":
			normalno = False
			break
	if normalno:
		orgs.append(new_org)
		write_in_file("Organizations", str(orgs).replace("\'", "\""))
	return render(request, "inventory/org_list.html", {"orgs": orgs})

def delete_org(request):
	act = request.POST.get("act")
	orgs = open_file("Organizations")
	org_name = request.POST.get("org_name")
	counter = 0;
	boolean = False
	# тру, если найдена организация с таким именем
	for org in orgs:
		if org["org_name"] == org_name:
			boolean = True
			break
		counter += 1
	if boolean:
		if act == "удалить организацию":
			orgs = orgs[:counter] + orgs[counter+1:]
			write_in_file("Organizations", str(orgs).replace("\'", "\""))
		elif act == "удалить ценность":
			return render(request, "inventory/delete_wealth.html", {"org": orgs[counter]})
	return render(request, "inventory/org_list.html", {"orgs": orgs})


def add_wealth(request):
	name = request.POST.get("org_name")
	orgs = open_file("Organizations")
	normalno = True
	for org in orgs:
		if org["org_name"] == name:
			new_w = {
				"name": request.POST.get("name"),
				"type": request.POST.get("type"),
				"owner": request.POST.get("owner"),
				"purchase_date": request.POST.get("purchase_date"),
				"description": request.POST.get("description")
			}
			for w in org["wealth"]:
				if w["name"] == new_w["name"] or new_w["name"] == "":
					normalno = False
					break
			if normalno:
				org["wealth"].append(new_w)
				write_in_file("Organizations", str(orgs).replace("\'", "\""))
	return render(request, "inventory/org_list.html", {"orgs": orgs})

def delete_wealth(request):
	orgs = open_file("Organizations")
	org_name = request.POST.get("org_name")
	name = request.POST.get("name")
	counter_org = -1
	boolean = False
	# тру, когда нашлась нужная ценность
	for org in orgs:
		counter_org += 1
		if org["org_name"] == org_name:
			counter_w = 0
			for w in org["wealth"]:
				print(w["name"])
				if w["name"] == name:
					boolean = True
					break
				counter_w += 1
			print('counter_org:', counter_org)
			print(orgs[counter_org])
			break
	if boolean:
		print(org["wealth"])
		org["wealth"] = org["wealth"][:counter_w] + org["wealth"][counter_w+1:]
		orgs = orgs[:counter_org] + [org] + orgs[counter_org+1:]
		write_in_file("Organizations", str(orgs).replace("\'", "\""))
	return render(request, "inventory/org_list.html", {"orgs": orgs})

def ap(request):
    return render(request, "inventory/auth_page.html")


def auth(request):
	act = request.POST.get("act")
	orgs = open_file("Organizations")
	if request.POST.get("login") == log_info["login"] and request.POST.get("password") == log_info["password"]:
		if act == "создать организацию":
			return render(request, "inventory/add_org.html", {})
		elif act == "добавить ценность":
			return render(request, "inventory/add_wealth.html", {"orgs": orgs})
		elif act == "удалить":
			return render(request, "inventory/delete_org.html", {"orgs": orgs})

	return render(request, "inventory/org_list.html", {"orgs": orgs})