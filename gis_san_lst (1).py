import re

def gis_san_lst_0(addr):

    san_lst = {'@' : '&',\
                'INTERSTATE 043 SOUTH/': '',\
                '1ST S / 4626': '4626 1ST ST',\
                'I 94/ 27TH ST N': 'W ST PAUL AVE & N 27TH ST',\
                '435 W AUER AVE / 435 W AUER AVE': '435 W AUER AVE',\
                'MEDFORD AVE W / RIDGE CT W': 'W MEDFORD AVE & W RIDGE CT',\
                'DR M L KING JR DR N / 3007 SB': 'N DOCTOR M.L.K. DR & 3007',\
                '3RD ST N / MC KINLEY ST': 'N OLD WORLD 3RD ST & W MCKINLEY AVE',\
                'FOND DU LAC AVE W / 4350 W FOND DU LAC AV': '4350 W FOND DU LAC AVE',\
                '3840 N DOCTOR M.L.K. DR / 3840 N DOCTOR M.L.K. DR': '3840 N DOCTOR M.L.K. DR',\
                '/': '&',\
                ' A 304 ': ' ',\
                ' AV 112 ': ' AVE ',\
                #'NB': '',\
                #'SB': '',\
                #'EB': '',\
                #'WB': '',\
                ' 4 ': ' ',\
                ' A ': ' ',\
                'BLK': '',\
                'BLV': 'BLVD',\
                'DRV': 'DR',\
                ' NB': '',\
                ' SB': '',\
                ' EB': '',\
                ' WB': '',\
                'NB ': '',\
                'SB ': '',\
                'EB ': '',\
                'WB ': '',\
                '6 ST': '6TH ST',\
                '6 TH': '6TH',\
                ' AV ': ' AVE ',\
                'BLCK': '',\
                'BLK ': '',\
                ' BLK': '',\
                'BLV ': 'BLVD ',\
                ' BLV': ' BLVD',\
                'DRV ': 'DR ',\
                ' DRV': ' DR',\
                ' NB ': '',\
                ' SB ': '',\
                ' EB ': '',\
                ' WB ': '',\
                '11 ST': '11TH ST',\
                '37 ST': '37TH ST',\
                '48 ST': '48TH ST',\
                '84 ST': '84TH ST',\
                '96 ST': '96TH ST',\
                ' BLK ': '',\
                'BLCK ': '',\
                ' BLCK': '',\
                'BLOCK': '',\
                ' BLV ': ' BLVD ',\
                ' DRV ': ' DR ',\
                ' STR ': ' ST ',\
                ' BLCK ': '',\
                'BLOCK ': '',\
                ' BLOCK': '',\
                'VLILET': 'VLIET',\
                ' BLOCK ': '',\
                'BREWER ': 'BREWERS WAY',\
                'N 27 ST': 'N 27TH ST',\
                'S 27 ST': 'S 27TH ST',\
                'MINERALD': 'MINERAL',\
                'N GRA RD': 'N GRANVILLE RD',\
                'OAK ST E': 'E OAK ST',\
                'OAK ST W': 'W OAK ST',\
                '101ST ST N':'N 101ST ST',\
                '92ND ST S': 'S 92ND ST',\
                '92ND ST N': 'N 92ND ST',\
                '91ST ST S': 'S 91ST ST',\
                '91ST ST N': 'N 91ST ST',\
                '86TH ST S': 'S 86TH ST',\
                '86TH ST N': 'N 86TH ST',\
                '85TH ST S': 'S 85TH ST',\
                '85TH ST N': 'N 85TH ST',\
                '84TH ST S': 'S 84TH ST',\
                '84TH ST N': 'N 84TH ST',\
                '82ND ST S': 'S 82ND ST',\
                '82ND ST N': 'N 82ND ST',\
                '81ST ST S': 'S 81ST ST',\
                '81ST ST N': 'N 81ST ST',\
                '80TH ST S': 'S 80TH ST',\
                '80TH ST N': 'N 80TH ST',\
                '79TH ST S': 'S 79TH ST',\
                '79TH ST N': 'N 79TH ST',\
                '78TH ST S': 'S 78TH ST',\
                '78TH ST N': 'N 78TH ST',\
                '77TH ST S': 'S 77TH ST',\
                '77TH ST N': 'N 77TH ST',\
                '76TH ST S': 'S 76TH ST',\
                '76TH ST N': 'N 76TH ST',\
                '75TH ST S': 'S 75TH ST',\
                '75TH ST N': 'N 75TH ST',\
                '72ND ST S': 'S 72ND ST',\
                '72ND ST N': 'N 72ND ST',\
                '68TH ST S': 'S 68TH ST',\
                '68TH ST N': 'N 68TH ST',\
                '62ND ST S': 'S 62ND ST',\
                '62ND ST N': 'N 62ND ST',\
                '61ST ST S': 'S 61ST ST',\
                '61ST ST N': 'N 61ST ST',\
                '60TH ST S': 'S 60TH ST',\
                '60TH ST N': 'N 60TH ST',\
                '59TH ST S': 'S 59TH ST',\
                '59TH ST N': 'N 59TH ST',\
                '58TH ST S': 'S 58TH ST',\
                '58TH ST N': 'N 58TH ST',\
                '57TH ST S': 'S 57TH ST',\
                '57TH ST N': 'N 57TH ST',\
                '56TH ST S': 'S 56TH ST',\
                '56TH ST N': 'N 56TH ST',\
                '55TH ST S': 'S 55TH ST',\
                '55TH ST N': 'N 55TH ST',\
                '52ND ST S': 'S 52ND ST',\
                '52ND ST N': 'N 52ND ST',\
                '51ST ST S': 'S 51ST ST',\
                '51ST ST N': 'N 51ST ST',\
                '50TH ST S': 'S 50TH ST',\
                '50TH ST N': 'N 50TH ST',\
                '49TH ST S': 'S 49TH ST',\
                '49TH ST N': 'N 49TH ST',\
                '45TH ST S': 'S 45TH ST',\
                '45TH ST N': 'N 45TH ST',\
                '44TH ST S': 'S 44TH ST',\
                '44TH ST N': 'N 44TH ST',\
                '43RD ST S': 'S 43RD ST',\
                '43RD ST N': 'N 43RD ST',\
                '42ND ST S': 'S 42ND ST',\
                '42ND ST N': 'N 42ND ST',\
                '41ST ST S': 'S 41ST ST',\
                '41ST ST N': 'N 41ST ST',\
                '40TH ST S': 'S 40TH ST',\
                '40TH ST N': 'N 40TH ST',\
                '39TH ST S': 'S 39TH ST',\
                '39TH ST N': 'N 39TH ST',\
                '38TH ST S': 'S 38TH ST',\
                '38TH ST N': 'N 38TH ST',\
                '37TH ST S': 'S 37TH ST',\
                '37TH ST N': 'N 37TH ST',\
                '36TH ST S': 'S 36TH ST',\
                '36TH ST N': 'N 36TH ST',\
                '35TH ST S': 'S 35TH ST',\
                '35TH ST N': 'N 35TH ST',\
                '34TH ST S': 'S 34TH ST',\
                '34TH ST N': 'N 34TH ST',\
                '33RD ST S': 'S 33RD ST',\
                '33RD ST N': 'N 33RD ST',\
                '32ND ST S': 'S 32ND ST',\
                '32ND ST N': 'N 32ND ST',\
                '31ST ST S': 'S 31ST ST',\
                '31ST ST N': 'N 31ST ST',\
                '30TH ST S': 'S 30TH ST',\
                '30TH ST N': 'N 30TH ST',\
                '29TH ST S': 'S 29TH ST',\
                '29TH ST N': 'N 29TH ST',\
                '28TH ST S': 'S 28TH ST',\
                '28TH ST N': 'N 28TH ST',\
                '27TH ST S': 'S 27TH ST',\
                '27TH ST N': 'N 27TH ST',\
                '26TH ST S': 'S 26TH ST',\
                '26TH ST N': 'N 26TH ST',\
                '25TH ST S': 'S 25TH ST',\
                '25TH ST N': 'N 25TH ST',\
                '24TH ST S': 'S 24TH ST',\
                '24TH ST N': 'N 24TH ST',\
                '23RD ST S': 'S 23RD ST',\
                '23RD ST N': 'N 23RD ST',\
                '22ND ST S': 'S 22ND ST',\
                '22ND ST N': 'N 22ND ST',\
                '21ST ST S': 'S 21ST ST',\
                '21ST ST N': 'N 21ST ST',\
                '20TH ST S': 'S 20TH ST',\
                '20TH ST N': 'N 20TH ST',\
                '19TH ST S': 'S 19TH ST',\
                '19TH ST N': 'N 19TH ST',\
                '18TH ST S': 'S 18TH ST',\
                '18TH ST N': 'N 18TH ST',\
                '17TH ST S': 'S 17TH ST',\
                '17TH ST N': 'N 17TH ST',\
                '16TH ST S': 'S 16TH ST',\
                '16TH ST N': 'N 16TH ST',\
                '15TH ST S': 'S 15TH ST',\
                '15TH ST N': 'N 15TH ST',\
                '15TH PL S': 'S 15TH PL',\
                '15TH PL N': 'N 15TH PL',\
                '14TH ST S': 'S 14TH ST',\
                '14TH ST N': 'N 14TH ST',\
                '13TH ST S': 'S 13TH ST',\
                '13TH ST N': 'N 13TH ST',\
                '12TH ST S': 'S 12TH ST',\
                '12TH ST N': 'N 12TH ST',\
                '11TH ST S': 'S 11TH ST',\
                '11TH ST N': 'N 11TH ST',\
                '10TH ST S': 'S 10TH ST',\
                '10TH ST N': 'N 10TH ST',\
                '9TH ST S': 'S 9TH ST',\
                '9TH ST N': 'N 9TH ST',\
                '9TH PL S': 'S 9TH PL',\
                '9TH PL N': 'N 9TH PL',\
                '8TH ST S': 'S 8TH ST',\
                '8TH ST N': 'N 8TH ST',\
                '7TH ST S': 'S 7TH ST',\
                '7TH ST N': 'N 7TH ST',\
                '6TH ST S': 'S 6TH ST',\
                '6TH ST N': 'N 6TH ST',\
                '5TH ST S': 'S 5TH ST',\
                '5TH ST N': 'N 5TH ST',\
                '4TH ST S': 'S 4TH ST',\
                '4TH ST N': 'N 4TH ST',\
                '2ND ST S': 'S 2ND ST',\
                '2ND ST N': 'N 2ND ST',\
                '1ST ST S': 'S 1ST ST',\
                '1ST ST N': 'N 1ST ST',\
                '1ST PL S': 'S 1ST PL',\
                '1ST PL N': 'N 1ST PL',\
                'KANE PL E': 'E KANE PL',\
                'KANE PL W': 'W KANE PL',\
                'MILL RD W': 'W MILL RD',\
                'RING ST E': 'E RING ST',\
                'RING ST W': 'W RING ST',\
                '5679 S 27': '5679 S 27TH ST',\
                'EASTBOUND': '',\
                'WESTBOUND': '',\
                'NORTHBOUND': '',\
                'SOUTHBOUND': '',\
                'AUER AVE E': 'E AUER AVE',\
                'AUER AVE W': 'W AUER AVE',\
                'S 27TH STR': 'S 27TH ST',\
                'BROWN ST E': 'E BROWN ST',\
                'BROWN ST W': 'W BROWN ST',\
                'HOPE AVE E': 'E HOPE AVE',\
                'HOPE AVE W': 'W HOPE AVE',\
                'HOLT AVE E': 'E HOLT AVE',\
                'HOLT AVE W': 'W HOLT AVE',\
                'KAUL AVE E': 'E KAUL AVE',\
                'KAUL AVE W': 'W KAUL AVE',\
                '100TH ST N': 'N 100TH ST',\
                '100TH ST S': 'S 100TH ST',\
                'KNAPP ST E': 'E KNAPP ST',\
                'KNAPP ST W': 'W KNAPP ST',\
                'LLOYD ST E': 'E LLOYD ST',\
                'LLOYD ST W': 'W LLOYD ST',\
                'MAPLE ST E': 'E MAPLE ST',\
                'MAPLE ST W': 'W MAPLE ST',\
                'OHIO AVE E': 'E OHIO AVE',\
                'OHIO AVE W': 'W OHIO AVE',\
                'OLIVE ST E': 'E OLIVE ST',\
                'OLIVE ST W': 'W OLIVE ST',\
                'PAINE ST E': 'E PAINE ST',\
                'PAINE ST W': 'W PAINE ST',\
                'PEARL ST N': 'N PEARL ST',\
                'PEARL ST S': 'S PEARL ST',\
                'RIDGE CT E': 'E RIDGE CT',\
                'RIDGE CT W': 'W RIDGE CT',\
                'SMITH ST E': 'E SMITH ST',\
                'SMITH ST W': 'W SMITH ST',\
                'STATE ST E': 'E STATE ST',\
                'STATE ST W': 'W STATE ST',\
                'VLIET ST E': 'E VLIET ST',\
                'VLIET ST W': 'W VLIET ST',\
                'WATER ST N': 'N WATER ST',\
                'WATER ST S': 'S WATER ST',\
                'WELLS ST E': 'E WELLS ST',\
                'WELLS ST W': 'W WELLS ST',\
                '58TH BLVD N': 'N 58TH BLVD',\
                '58TH BLVD S': 'S 58TH BLVD',\
                ' ALLEY REAR': '',\
                'AUSTIN ST N': 'N AUSTIN ST',\
                'AUSTIN ST S': 'S AUSTIN ST',\
                'CHASE AVE N': 'N CHASE AVE',\
                'CHASE AVE S': 'S CHASE AVE',\
                'FLAGG AVE E': 'E FLAGG AVE',\
                'FLAGG AVE W': 'W FLAGG AVE',\
                'HAYES AVE E': 'E HAYES AVE',\
                'HAYES AVE W': 'W HAYES AVE',\
                'NORTH AVE E': 'E NORTH AVE',\
                'NORTH AVE W': 'W NORTH AVE',\
                'BECHER ST E': 'E BECHER ST',\
                'BECHER ST W': 'W BECHER ST',\
                'BUFFUM ST N': 'N BUFFUM ST',\
                'BUFFUM ST S': 'S BUFFUM ST',\
                'CENTER ST E': 'E CENTER ST',\
                'CENTER ST W': 'W CENTER ST',\
                'CHERRY ST E': 'E CHERRY ST',\
                'CHERRY ST W': 'W CHERRY ST',\
                'DAKOTA ST E': 'E DAKOTA ST',\
                'DAKOTA ST W': 'W DAKOTA ST',\
                'GALENA ST E': 'E GALENA ST',\
                'GALENA ST W': 'W GALENA ST',\
                'HADLEY ST E': 'E HADLEY ST',\
                'HADLEY ST W': 'W HADLEY ST',\
                'HAWLEY RD N': 'N HAWLEY RD',\
                'HAWLEY RD S': 'S HAWLEY RD',\
                'HOLTON ST N': 'N HOLTON ST',\
                'HOLTON ST S': 'S HOLTON ST',\
                'N 16TH REAR': 'N 16TH ST',\
                'LAPHAM ST E': 'E LAPHAM ST',\
                'LAPHAM ST W': 'W LAPHAM ST',\
                'LOCUST ST E': 'E LOCUST ST',\
                'LOCUST ST W': 'W LOCUST ST',\
                'PALMER ST N': 'N PALMER ST',\
                'PALMER ST S': 'S PALMER ST',\
                'ROGERS ST E': 'E ROGERS ST',\
                'ROGERS ST W': 'S ROGERS ST',\
                'SELIG DRIVE': 'SELIG DR',\
                'WALNUT ST E': 'E WALNUT ST',\
                'WALNUT ST W': 'W WALNUT ST',\
                'E WESTER PL': 'E WEBSTER PL',\
                'WRIGHT ST E': 'E WRIGHT ST',\
                'WRIGHT ST W': 'W WRIGHT ST',\
                'ARMOUR AVE E': 'E ARMOUR AVE',\
                'ARMOUR AVE W': 'W ARMOUR AVE',\
                'BARCLAY ST N': 'N BARCLAY ST',\
                'BARCLAY ST S': 'S BARCLAY ST',\
                'BURNHAM ST E': 'E BURNHAM ST',\
                'BURNHAM ST W': 'W BURNHAM ST',\
                'DAKOTA AVE E': 'E DAKOTA AVE',\
                'DAKOTA AVE W': 'W DAKOTA AVE',\
                'MINERAL ST E': 'E MINERAL ST',\
                'MINERAL ST W': 'W MINERAL ST',\
                'CAPITOL DR E': 'E CAPITOL DR',\
                'CAPITOL DR W': 'W CAPITOL DR',\
                'JUNEAU AVE E': 'E JUNEAU AVE',\
                'JUNEAU AVE W': 'W JUNEAU AVE',\
                'LISBON AVE E': 'E LISBON AVE',\
                'LISBON AVE W': 'W LISBON AVE',\
                'MELVINA ST E': 'E MELVINA ST',\
                'MELVINA ST W': 'W MELVINA ST',\
                'GRANT BLVD N': 'N GRANT BLVD',\
                'HANSON AVE N': 'N HANSON AVE',\
                'HANSON AVE S': 'S HANSON AVE',\
                'HOPKINS ST N': 'N HOPKINS ST',\
                'HOPKINS ST S': 'S HOPKINS ST',\
                'HOWARD AVE E': 'E HOWARD AVE',\
                'HOWARD AVE W': 'W HOWARD AVE',\
                'HOWELL AVE N': 'N HOWELL AVE',\
                'HOWELL AVE S': 'S HOWELL AVE',\
                'LAYTON AVE E': 'E LAYTON AVE',\
                'LAYTON AVE W': 'W LAYTON AVE',\
                'MORGAN AVE E': 'E MORGAN AVE',\
                'MORGAN AVE W': 'W MORGAN AVE',\
                'SERVITE DR N': 'N SERVITE DR',\
                'SERVITE DR S': 'S SERVITE DR',\
                'SILVERSPRING': 'SILVER SPRING',\
                'WEBSTER PL E': 'E WEBSTER PL',\
                'WEBSTER PL W': 'W WEBSTER PL',\
                'BROOKLYN PL E': 'E BROOKLYN PL',\
                'BROOKLYN PL W': 'W BROOKLYN PL',\
                'BURLEIGH ST E': 'E BURLEIGH ST',\
                'BURLEIGH ST W': 'W BURLEIGH ST',\
                'CHAMBERS ST E': 'E CHAMBERS ST',\
                'CHAMBERS ST W': 'W CHAMBERS ST',\
                'CLYBOURN ST E': 'E CLYBOURN ST',\
                'CLYBOURN ST W': 'W CLYBOURN ST',\
                'CONGRESS ST E': 'E CONGRESS ST',\
                'CONGRESS ST W': 'W CONGRESS ST',\
                'ESTABROOK BLV': 'W ESTABROOK BLVD',\
                'FLORIST AVE E': 'E FLORIST AVE',\
                'FLORIST AVE W': 'W FLORIST AVE',\
                'GRANTOSA DR W': 'W GRANTOSA DR',\
                'HAMPTON AVE E': 'E HAMPTON AVE',\
                'HAMPTON AVE W': 'W HAMPTON AVE',\
                'LAYTON BLVD N': 'N LAYTON BLVD',\
                'LAYTON BLVD S': 'S LAYTON BLVD',\
                'LINCOLN AVE E': 'E LINCOLN AVE',\
                'LINCOLN AVE W': 'W LINCOLN AVE',\
                'MARSHALL ST N': 'N MARSHALL ST',\
                'MARSHALL ST S': 'S MARSHALL ST',\
                'MEDFORD AVE E': 'E MEDFORD AVE',\
                'MEDFORD AVE W': 'W MEDFORD AVE',\
                'MEREDITH ST E': 'E MEREDITH ST',\
                'MEREDITH ST W': 'W MEREDITH ST',\
                'MICHIGAN ST E': 'E MICHIGAN ST',\
                'MICHIGAN ST W': 'W MICHIGAN ST',\
                'MITCHELL ST E': 'E MITCHELL ST',\
                'MITCHELL ST W': 'W MITCHELL ST',\
                'OKLAHOMA PL W': 'W OKLAHOMA PL',\
                'OKLAHOMA PL W': 'W OKLAHOMA PL',\
                'RICHARDS ST N': 'N RICHARDS ST',\
                'RICHARDS ST S': 'S RICHARDS ST',\
                'SCRANTON PL E': 'E SCRANTON PL',\
                'SCRANTON PL W': 'W SCRANTON PL',\
                'VILLARD AVE E': 'E VILLARD AVE',\
                'VILLARD AVE W': 'W VILLARD AVE',\
                '3613 N 58TH BL': '3613 N 58TH BLVD',\
                'APPLETON AVE W': 'W APPLETON AVE',\
                'APPLETON AVE E': 'E APPLETON AVE',\
                'BOBOLINK AVE E': 'E BOBOLINK AVE',\
                'BOBOLINK AVE W': 'W BOBOLINK AVE',\
                'DELAWARE AVE N': 'N DELAWARE AVE',\
                'DELAWARE AVE S': 'S DELAWARE AVE',\
                'EDGERTON AVE E': 'E EDGERTON AVE',\
                'EDGERTON AVE W': 'W EDGERTON AVE',\
                'EVERGREEN LN E': 'E EVERGREEN LN',\
                'EVERGREEN LN W': 'W EVERGREEN LN',\
                'FONDULAC AVE E': 'E FOND DU LAC AVE',\
                'FONDULAC AVE W': 'W FOND DU LAC AVE',\
                'GARFIELD AVE E': 'E GARFIELD AVE',\
                'GARFIELD AVE W': 'W GARFIELD AVE',\
                'GOOD HOPE RD E': 'E GOOD HOPE RD',\
                'GOOD HOPE RD W': 'W GOOD HOPE RD',\
                'HIGHLAND AVE E': 'E HIGHLAND AVE',\
                'HIGHLAND AVE W': 'W HIGHLAND AVE',\
                'KILBOURN AVE E': 'E KILBOURN AVE',\
                'KILBOURN AVE W': 'W KILBOURN AVE',\
                'LAKEFIELD DR E': 'E LAKEFIELD DR',\
                'LAKEFIELD DR W': 'W LAKEFIELD DR',\
                'MEINECKE AVE E': 'E MEINECKE AVE',\
                'MEINECKE AVE W': 'W MEINECKE AVE',\
                'MILWAUKEE RD E': 'E MILWAUKEE RD',\
                'MILWAUKEE RD W': 'W MILWAUKEE RD',\
                'NATIONAL AVE E': 'E NATIONAL AVE',\
                'NATIONAL AVE W': 'W NATIONAL AVE',\
                'OKLAHOMA AVE E': 'E OKLAHOMA AVE',\
                'OKLAHOMA AVE W': 'W OKLAHOMA AVE',\
                'SHERMAN BLVD N': 'N SHERMAN BLVD',\
                'SHERMAN BLVD S': 'S SHERMAN BLVD',\
                'TEUTONIA AVE N': 'N TEUTONIA AVE',\
                'TEUTONIA AVE S': 'S TEUTONIA AVE',\
                'THURSTON AVE E': 'E THURSTON AVE',\
                'THURSTON AVE W': 'W THURSTON AVE',\
                'WINDLAKE AVE E': 'E WINDLAKE AVE',\
                'WINDLAKE AVE W': 'W WINDLAKE AVE',\
                'WISCONSIN AV E': 'E WISCONSIN AVE',\
                'WISCONSIN AV W': 'W WISCONSIN AVE',\
                'JEFFERSON ST N': 'N JEFFERSON ST',\
                'JEFFERSON ST S': 'S JEFFERSON ST',\
                'ROOSEVELT DR E':'E ROOSEVELT DR',\
                'ROOSEVELT DR W':'W ROOSEVELT DR',\
                'CLEVELAND AVE E': 'E CLEVELAND AVE',\
                'CLEVELAND AVE W': 'W CLEVELAND AVE',\
                'HUMBOLDT BLVD N': 'N HUMBOLDT BLVD',\
                'HUMBOLDT BLVD S': 'S HUMBOLDT BLVD',\
                'KENILWORTH PL E': 'E KENILWORTH PL',\
                'KENILWORTH PL W': 'W KENILWORTH PL',\
                'TROWBRIDGE ST E': 'E TROWBRIDGE ST',\
                'TROWBRIDGE ST W': 'W TROWBRIDGE ST',\
                'WATERFORD AVE E': 'E WATERFORD AVE',\
                'WATERFORD AVE W': 'W WATERFORD AVE',\
                'WISCONSIN AVE E': 'E WISCONSIN AVE',\
                'WISCONSIN AVE W': 'W WISCONSIN AVE',\
                'WASHINGTON ST E': 'E WASHINGTON ST',\
                'WASHINGTON ST W': 'W WASHINGTON ST',\
                'FREDERICK MI WAY': 'FREDERICK MILLER WAY',\
                'GREENFIELD AVE E': 'E GREENFIELD AVE',\
                'GREENFIELD AVE W': 'W GREENFIELD AVE',\
                'KEEFE AVE PKWY E': 'E KEEFE AVE PKWY',\
                'KEEFE AVE PKWY W': 'W KEEFE AVE PKWY',\
                'PLAINFIELD AVE E': 'E PLAINFIELD AVE',\
                'PLAINFIELD AVE W': 'W PLAINFIELD AVE',\
                'PRIVATE PROPERTY': '',\
                'W FON DU LAC AVE': 'W FOND DU LAC AV',\
                'N CESAR CHAVEZ DR': 'N CESAR E CHAVEZ DR',\
                'S CESAR CHAVEZ DR': 'S CESAR E CHAVEZ DR',\
                'FOND DU LAC AVE E': 'E FOND DU LAC AVE',\
                'FOND DU LAC AVE W': 'W FOND DU LAC AVE',\
                'FOREST HOME AVE E': 'E FOREST HOME AVE',\
                'FOREST HOME AVE W': 'W FOREST HOME AVE',\
                '5020 W CAPITOL DRV': '5020 W CAPITOL DR',\
                'KINNICKINNIC AVE N': 'N KINNICKINNIC AVE',\
                'KINNICKINNIC AVE S': 'S KINNICKINNIC AVE',\
                'OLD WORLD 3RD ST N': 'N OLD WORLD 3RD ST',\
                'OLD WORLD 3RD ST S': 'S OLD WORLD 3RD ST',\
                'SILVER SPRING DR E': 'E SILVER SPRING DR',\
                'SILVER SPRING DR W': 'W SILVER SPRING DR',\
                'CESAR E CHAVEZ DR N': 'N CESAR E CHAVEZ DR',\
                'CESAR E CHAVEZ DR S': 'S CESAR E CHAVEZ DR',\
                'MARTIN L KING JR DR': 'DOCTOR M.L.K. DR',\
                'N PORTWASHINGTON AV': 'N PORT WASHINGTON AVE',\
                'S PORTWASHINGTON AV': 'S PORT WASHINGTON AVE',\
                'O CONNER FRONTAGE RD': 'O CONNOR ST',\
                'OLD WORLD THIRD ST N': 'N OLD WORLD THIRD ST',\
                'OLD WORLD THIRD ST S': 'S OLD WORLD THIRD ST',\
                'PORT WASHINGTON AVE N': 'N PORT WASHINGTON AVE',\
                'PORT WASHINGTON AVE S': 'S PORT WASHINGTON AVE',\
                'MARTIN LUTHER KING DR': 'DOCTOR M.L.K. DR',\
                'SHERMAN CONNECTOR RDS': 'SHERMAN BLVD',\
                'HISTORIC MITCHELL ST E': 'E HISTORIC MITCHELL ST',\
                'HISTORIC MITCHELL ST W': 'W HISTORIC MITCHELL ST',\
                'ESTABROOK PARK PARK RD': 'ESTABROOK PKWY',\
                'MARTIN LUTHER KING J DRV': 'DOCTOR M.L.K. DR',\
                'DR MARTIN LUTHER KING JR DR': 'DOCTOR M.L.K. DR',\
                'LINCOLN CREEK PKWY W PARK RD': 'LINCOLN CREEK PKWY',\
                'LIT MEN RIVER PKWY N PARK RD': 'LITTLE MENOMONEE RIVER PKWY',\
                'BECHER ST W & 2523': '2523 W BECHER ST W',\
                #'GREEN BAY AVE N / I 43 EXIT RAMP': 'N GREEN BAY AVE & W FIE
                
#Katy's addition, please skim for review
                'AUER AVE E':'E AUER AVE',\
                'AUER AVE W':'W AUER AVE',\
                'BARCLAY ST S': 'S BARCLAY ST',\
                'BARCLAY ST' : 'S BARCLAY ST',\
                'BREWER ':'BREWERS WAY',\
                'BOBOLINK AVE W':'W AVE BOBOLINK',\
                'ESTABROOK PARK PARK RD' : 'ESTABROOK PKWY',\
                'ESTABROOK BLV': 'W ESTABROOK BLV',\
                'FARWELL AVE N':'N FARWELL AVE',\
                'FREDERICK MI WAY':'FREDERICK MILLER WAY',\
                'GRANT BLVD N' : 'N GRANT BLVD',\
                'GRANTOSA DR W':'W GRANTOSA DR',\
                'MILL RD W':'W MILL RD',\
                'LAFAYETTE PL E':'E LAFAYETTE PL',\
                'LIT MEN RIVER PKWY N PARK RD':'MENOMONEE RIVER PKWY',\
                'SILVERSPRING':'SILVER SPRING',\
                'ST PAUL AVE W':'W ST PAUL AVE',\
                'WOODSTOCK PL E':'E WOODSTOCK PL',\
                '6 ST':'6TH ST',\
                '11 ST':'11TH ST',\
                '37 ST':'37TH ST',\
                '48 ST':'48TH ST',\
                '84 ST':'84TH ST',\
                '96 ST':'96TH ST',\
                '@':'&',\
                'ON ':'',\
                '4471 & N 60TH ST':'4471 N 60TH ST',\
                'HOYT PL W':'W HOYT PL',\
                'EUCLID AVE W':'W EUCLID AVE',\
                'FALKNER':'FAULKNER',\
                '3475 & N 27TH ST':'3475 N 27TH ST',\
                '3620 & N 27TH ST': '3620 N 27TH ST',\
                'PRIVATE PROPERTY':'',\
                ',MKE':'MILWAUKEE, WISCONSIN'\

 }

    pattern = re.compile('|'.join(san_lst.keys()))
    #pattern = re.compile(r'\b(' + '|'.join(san_lst.keys()) + r')\b')
    result = pattern.sub(lambda x: san_lst[x.group()], addr)
    return result

def gis_san_lst_1(addr):

    san_lst = {'BECHER ST W & 2523': '2523 W BECHER ST W',\
                'CESAR CHAVEZ & 1633 S': '1633 S CESAR E CHAVEZ DR',\
                'E HOWARD AVE & 200': '200 E HOWARD AVE',\
                'E NORTH AVE & 1609': '1609 E NORTH AVE',\
                'N 20TH ST & 900': '900 N 20TH ST',\
                'N 27TH ST & 1500': '1500 N 27TH ST',\
                'N 27TH ST & 1900': '1900 N 27TH ST',\
                'N 27TH ST & 900': '900 N 27TH ST',\
                'N 32ND ST & 2200': '2200 N 32ND',\
                'N 35TH ST & 400': '400 N 35TH',\
                'N 35TH ST & 900': '900 N 35TH',\
                'N 36TH ST & 2200': '2200 N 36TH ST',\
                'N 37TH ST & 1700': '1700 N 37TH ST',\
                'N 40TH ST & 1819 N': '1819 N 40TH ST',\
                'N 42ND ST & 1300': '1300 N 42ND ST',\
                'N SHERMAN BLVD & 2100': '2100 N SHERMAN BLVD',\
                'N 35TH ST & 2200': '2200 N 35TH',\
                'S 13TH ST & 1600': '1600 S 13TH ST',\
                'S 13TH ST & 3900': '3900 S 13TH ST',\
                'S 13TH ST & 4700': '4700 S 13TH ST',\
                'S 13TH ST & 5200': '5200 S 13TH ST',\
                'S 18TH ST & 1209': '1209 S 18TH ST',\
                'S 1ST ST & 2011': '2011 S 1ST ST',\
                'S 20TH ST & 3900': '3900 S 20TH ST',\
                'S 27TH ST & 4278': '4278 S 27TH ST',\
                'S 31ST ST & 700': '700 S 31ST ST',\
                'S 43RD ST & 2700': '2700 S 43RD ST',\
                'S HOWELL AVE & 4368': '4368 S HOWELL AVE',\
                'S LAYTON BLVD & 1619': '1619 S LAYTON BLVD',\
                'W BECHER ST & 2523': '2523 W BECHER ST',\
                'W CAPITOL DR & 2700': '2700 W CAPITOL DR',\
                'W CENTER ST & 2900':'2900 W CENTER ST',\
                'W CENTER ST & 3900':'3900 W CENTER ST',\
                'W CONGRESS ST & 6730': '6730 W CONGRESS ST',\
                'W EDGERTON AVE & 1800': '1800 W EDGERTON AVE',\
                'W FOND DU LAC AVE & 4400': '4400 W FOND DU LAC AVE',\
                'W FOND DU LAC AVE & 4729': '4729 W FOND DU LAC AVE',\
                'W FOREST HOME AVE & 4300': '4300 W FOREST HOME AVE',\
                'W HIGHLAND AVE & 2400': '2400 W HIGHLAND AVE',\
                'S 16TH ST & W LAPHAM ST': 'S CESAR E CHAVEZ DR & W LAPHAM ST',\
                'W LAYTON AVE & 100': '100 W LAYTON AVE',\
                'W LINCOLN AVE & 2500': '2500 W LINCOLN AVE',\
                'W LISBON AVE & 3000': '3000 W LISBON AVE',\
                'W LISBON AVE & 3100': '3100 W LISBON AVE',\
                'W LISBON AVE & 3700': '3700 W LISBON AVE',\
                'W LISBON AVE & 5800': '5800 W LISBON AVE',\
                'W LOCUST ST & 5N 8TH': 'W LOCUST ST & N 58TH ST',\
                'W MITCHELL ST & 2109': '2109 W MITCHELL ST',\
                'W NATIONAL AVE & 2600': '2600 W NATIONAL AVE',\
                'W OKLAHOMA AVE & 3422': '3422 W OKLAHOMA AVE',\
                'W VLIET ST & 3500':'3500 W VLIET ST',\
                'W VILLARD AVE & 3629':'3629 W VILLARD AVE',\
                'W WISCONSIN AVE & 3900': '3900 W WISCONSIN AVE',\
                'W WISCONSIN AVE & 4200': '4200 W WISCONSIN AVE',\
                '5010 N 37TH ST &': '5010 N 37TH ST',\
                'N 51ST ST & 4500':'4500 N 51ST ST',\

                #Laura's addition 6/21
                '517 N 33 RD ST REAR OF ':'517 N 33RD ST',\
                'WIS':'WISCONSIN',\
                '#108':'',\
                '100TH REAR':'100TH ST',\
                '3908 N ST':'3908 N 83RD ST',\
                '3001 E LINWOOD':'3001 E LINNWOOD AVE',\
                'PLEASANT ST BRIDGE &':'372 E PLEASANT ST',\
                '1018 W GREENFIELD AVE REAR':'1018 W GREENFIELD AVE',\
                '8350 N STEVENS':'8350 N STEVEN RD',\
                '2605 W VICTOR LN':'2605 W VICTORY LN',\
                }

    pattern = re.compile('|'.join(san_lst.keys()))
    #pattern = re.compile(r'\b(' + '|'.join(san_lst.keys()) + r')\b')
    result = pattern.sub(lambda x: san_lst[x.group()], addr)
    return result
