# Shamelessly stolen here: 
# https://stackoverflow.com/questions/44442750/inner-looping-with-terraform#44463687

#provider "github" {
#  token        = "${var.github_token}"
#  organization = "${var.github_organization}"
#}

module "team1" {
  source = "./team"
  name = "team1"
  description = "Team N1"
  members = [ "user1","user3","user5","user6","user7","user8","user9","user10" ]
  maintainers = [ "user2" ]
}

module "team2" {
  source = "./team"
  name = "team2"
  description = "Team N2"
  members = [ "user2","user3","user4","user6","user7","user8","user9","user10" ]
  maintainers = [ "user1" ]
}

module "team3" {
  source = "./team"
  name = "team3"
  description = "Team N3"
  members = [ "user1","user2","user4","user5","user6","user7" ]
  maintainers = [ "user3" ]
}

module "team4" {
  source = "./team"
  name = "team4"
  description = "Team N4"
  members = [ "user1","user3","user4","user5","user6","user7","user8","user9","user10" ]
  maintainers = [ "user2" ]
}

module "team5" {
  source = "./team"
  name = "team5"
  description = "Team N5"
  members = ["user2","user3","user4","user6","user7","user8","user9","user10" ]
  maintainers = [ "user1" ]
}

module "team6" {
  source = "./team"
  name = "team6"
  description = "Team N6"
  members = [ "user1","user2","user3","user5","user7","user8","user9","user10" ]
  maintainers = [ "user4" ]
}

