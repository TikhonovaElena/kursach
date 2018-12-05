from django.shortcuts import render
import sys, string, os, json
from .models import Post


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
		"description": request.POST.get("description"),
		"director_first_name": request.POST.get("director_first_name"),
		"director_last_name": request.POST.get("director_last_name"),
		"director_middle_name": request.POST.get("director_middle_name"),
		"director_DOB": request.POST.get("director_DOB"),
		"wealth": [{
			"name": "",
			"type": "",
			"owner": "",
			"purchase_date": "",
			"description": ""
		}]
	}
	orgs.append(new_org)
	write_in_file("Organizations", str(orgs).replace("\'", "\""))
	return render(request, "inventory/org_list.html", {"orgs": orgs})


def add_wealth(request):
	print(request.POST.get("org_name"))

	orgs = open_file("Organizations")
	for org in orgs:
		if org["org_name"] == request.POST.get("org_name"):
			w = {
				"name": request.POST.get("name"),
				"type": request.POST.get("type"),
				"owner": request.POST.get("owner"),
				"purchase_date": request.POST.get("purchase_date"),
				"description": request.POST.get("description")
			}
			org["wealth"].append(w)
			write_in_file("Organizations", str(orgs).replace("\'", "\""))
	return render(request, "inventory/org_list.html", {"orgs": orgs})


def set_wealth(request):
	log_info = {"login": "root", "password": "root"}

	if request.POST.get("login") == log_info["login"] and request.POST.get("password") == log_info["password"]:
		return render(
			request, "inventory/add_wealth.html",
			{"info": {"org_name": request.POST.get("org_name")}})

	orgs = open_file("Organizations")
	return render(request, "inventory/org_list.html", {"orgs": orgs})


def auth(request):
	log_info = {"login": "root", "password": "root"}
	if request.POST.get("login") == log_info["login"] and request.POST.get("password") == log_info["password"]:
		return render(request, "inventory/admin_editing.html", {})

	orgs = open_file("Organizations")
	return render(request, "inventory/org_list.html", {"orgs": orgs})