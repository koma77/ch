variable "name" {
}

variable "description" {
} 

variable "members" {
  type = "list"
}

variable "maintainers" {
  type = "list"
}


resource "github_team" "this" {
  name        = "${var.name}"
  description = "${var.description}"
}

resource "github_team_membership" "members" {
  count = "${length(var.members)}"
  team_id  = "${github_team.this.id}"
  username = "${var.members[count.index]}"
  role     = "member"
}

resource "github_team_membership" "maintainers" {
  count = "${length(var.maintainers)}"
  team_id  = "${github_team.this.id}"
  username = "${var.maintainers[count.index]}"
  role     = "maintainer"
}
