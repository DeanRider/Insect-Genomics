Submit-block ::= {
  contact {
    contact {
      name name {
        last "Doe",
        first "John",
        middle "",
        initials "",
        suffix "",
        title ""
      },
      affil std {
        affil "Fancy Place",
        div "Bigger Department",
        city "Anytown",
        sub "DN",
        country "Atlantis",
        street "123 Main Street",
        email "professor@university.ed",
        postal-code "99999"
      }
    }
  },
  cit {
    authors {
      names std {
        {
          name name {
            last "Doe",
            first "John",
            middle "",
            initials "P.",
            suffix "",
            title ""
          }
        }
      },
      affil std {
        affil "Fancy Place",
        div "Bigger Department",
        city "Anytown",
        sub "DN",
        country "Atlantis",
        street "123 Main Street",
        postal-code "99999"
      }
    }
  },
  subtype new
}
Seqdesc ::= pub {
  pub {
    gen {
      cit "unpublished",
      authors {
        names std {
          {
            name name {
              last "Doe",
              first "John",
              middle "",
              initials "P.",
              suffix "",
              title ""
            }
          }
        }
      },
      title "Test Genome for Interpro Domains"
    }
  }
}
Seqdesc ::= user {
  type str "Submission",
  data {
    {
      label str "AdditionalComment",
      data str "ALT EMAIL:professor@university.ed"
    }
  }
}
Seqdesc ::= user {
  type str "Submission",
  data {
    {
      label str "AdditionalComment",
      data str "Submission Title:None"
    }
  }
}
