from models.player import Player
from models.team import Team
import services.team_repository as team_repo

# COLO-COLO (Plantel 2026 tras salidas a Europa y nuevos fichajes)
colo_colo = Team("Colo-Colo")

colo_colo.add_player(Player("Fernando de Paul", 35, 77, 15, 85, "GK"))
colo_colo.add_player(Player("Jeyson Rojas", 24, 74, 55, 75, "FB"))
colo_colo.add_player(Player("Jonathan Villagra", 25, 76, 30, 84, "CB"))
colo_colo.add_player(Player("Joaquin Sosa", 24, 76, 35, 82, "CB"))
colo_colo.add_player(Player("Erick Wiemberg", 31, 76, 65, 76, "FB"))
colo_colo.add_player(Player("Victor Mendez", 26, 78, 75, 75, "CM"))
colo_colo.add_player(Player("Tomas Alarcon", 27, 77, 65, 82, "CDM"))
colo_colo.add_player(Player("Arturo Vidal", 39, 81, 82, 74, "CM"))
colo_colo.add_player(Player("Claudio Aquino", 34, 78, 85, 50, "CAM"))
colo_colo.add_player(Player("Maximiliano Romero", 27, 77, 82, 35, "ST"))
colo_colo.add_player(Player("Javier Correa", 33, 78, 84, 30, "ST"))

team_repo.save_team(colo_colo)

# UNIVERSIDAD DE CHILE (Con los retornos estelares y compras definitivas)
u_de_chile = Team("Universidad de Chile")

u_de_chile.add_player(Player("Gabriel Castellon", 32, 78, 12, 86, "GK"))
u_de_chile.add_player(Player("Fabian Hormazabal", 30, 77, 65, 76, "FB"))
u_de_chile.add_player(Player("Franco Calderon", 28, 77, 32, 85, "CB"))
u_de_chile.add_player(Player("Matias Zaldivia", 35, 77, 35, 83, "CB"))
u_de_chile.add_player(Player("Marcelo Morales", 23, 78, 70, 74, "FB"))
u_de_chile.add_player(Player("Marcelo Diaz", 39, 76, 68, 78, "CDM"))
u_de_chile.add_player(Player("Charles Aranguiz", 37, 79, 78, 76, "CM"))
u_de_chile.add_player(Player("Lucas Romero", 23, 75, 60, 79, "CDM"))
u_de_chile.add_player(Player("Javier Altamirano", 26, 78, 79, 55, "CAM"))
u_de_chile.add_player(Player("Eduardo Vargas", 36, 78, 84, 35, "ST"))
u_de_chile.add_player(Player("Maximiliano Guerrero", 26, 77, 82, 45, "WNG"))

team_repo.save_team(u_de_chile)

# UNIVERSIDAD CATÓLICA (Plantel renovado 2026 dirigido por Daniel Garnero)
u_catolica = Team("Universidad Catolica")

u_catolica.add_player(Player("Vicente Bernedo", 25, 74, 10, 82, "GK"))
u_catolica.add_player(Player("Bernardo Cerezo", 30, 75, 58, 74, "FB"))
u_catolica.add_player(Player("Branco Ampuero", 32, 76, 30, 82, "CB"))
u_catolica.add_player(Player("Daniel Gonzalez", 23, 75, 32, 80, "CB"))
u_catolica.add_player(Player("Cristian Cuevas", 31, 75, 68, 68, "FB"))
u_catolica.add_player(Player("Gary Medel", 38, 77, 45, 84, "CB"))
u_catolica.add_player(Player("Jhojan Valencia", 29, 75, 55, 80, "CDM"))
u_catolica.add_player(Player("Matias Palavecino", 28, 76, 78, 55, "CAM"))
u_catolica.add_player(Player("Clemente Montes", 25, 75, 81, 40, "WNG"))
u_catolica.add_player(Player("Justo Giani", 27, 74, 78, 42, "WNG"))
u_catolica.add_player(Player("Fernando Zampedri", 38, 81, 86, 35, "ST"))

team_repo.save_team(u_catolica)

# PALESTINO
palestino = Team("Palestino")

palestino.add_player(Player("Cesar Rigamonti", 38, 76, 12, 82, "GK"))
palestino.add_player(Player("Benjamin Rojas", 25, 74, 60, 72, "FB"))
palestino.add_player(Player("Cristian Suarez", 39, 74, 35, 78, "CB"))
palestino.add_player(Player("Ivan Roman", 19, 75, 30, 80, "CB"))
palestino.add_player(Player("Dilan Zuñiga", 30, 74, 62, 70, "FB"))
palestino.add_player(Player("Ariel Martinez", 32, 74, 72, 68, "CM"))
palestino.add_player(Player("Misael Davila", 35, 75, 74, 65, "CM"))
palestino.add_player(Player("Joe Abrigo", 31, 75, 78, 50, "CAM"))
palestino.add_player(Player("Bryan Carrasco", 35, 75, 80, 45, "WNG"))
palestino.add_player(Player("Junior Marabel", 28, 74, 78, 35, "ST"))
palestino.add_player(Player("Gonzalo Sosa", 37, 75, 79, 38, "ST"))

team_repo.save_team(palestino)

# COQUIMBO UNIDO
coquimbo = Team("Coquimbo Unido")

coquimbo.add_player(Player("Diego Sanchez", 39, 75, 15, 80, "GK"))
coquimbo.add_player(Player("Dylan Escobar", 25, 74, 60, 70, "FB"))
coquimbo.add_player(Player("Bruno Cabrera", 29, 74, 30, 77, "CB"))
coquimbo.add_player(Player("Manuel Fernandez", 37, 73, 28, 76, "CB"))
coquimbo.add_player(Player("Sebastian Cabrera", 28, 74, 62, 71, "FB"))
coquimbo.add_player(Player("Alejandro Camargo", 37, 75, 55, 78, "CDM"))
coquimbo.add_player(Player("Dylan Glaby", 29, 76, 65, 79, "CM"))
coquimbo.add_player(Player("Juan Manuel Vazquez", 31, 74, 75, 55, "CAM"))
coquimbo.add_player(Player("Cristian Zavala", 26, 76, 82, 42, "WNG"))
coquimbo.add_player(Player("Andres Chavez", 35, 74, 78, 35, "ST"))
coquimbo.add_player(Player("Jonatan Bauman", 35, 74, 77, 32, "ST"))

team_repo.save_team(coquimbo)

# EVERTON
everton = Team("Everton")

everton.add_player(Player("Ignacio Gonzalez", 36, 75, 12, 81, "GK"))
everton.add_player(Player("Felipe Campos", 32, 74, 55, 75, "FB"))
everton.add_player(Player("Diego Oyarzun", 33, 74, 32, 78, "CB"))
everton.add_player(Player("Eduardo Bauermann", 30, 76, 35, 80, "CB"))
everton.add_player(Player("Alex Ibacache", 27, 75, 65, 72, "FB"))
everton.add_player(Player("Alvaro Madrid", 31, 76, 72, 74, "CM"))
everton.add_player(Player("Benjamin Berrios", 28, 75, 70, 73, "CM"))
everton.add_player(Player("Federico Martinez", 30, 75, 79, 45, "WNG"))
everton.add_player(Player("Rodrigo Contreras", 30, 77, 82, 35, "ST"))
everton.add_player(Player("Kevin Mendez", 30, 74, 77, 48, "WNG"))
everton.add_player(Player("Lautaro Pastran", 24, 75, 78, 40, "WNG"))

team_repo.save_team(everton)

# AUDAX ITALIANO
audax = Team("Audax Italiano")

audax.add_player(Player("Tomas Ahumada", 24, 74, 10, 80, "GK"))
audax.add_player(Player("Nicolas Fernandez", 27, 74, 60, 70, "FB"))
audax.add_player(Player("German Guiffrey", 28, 74, 30, 76, "CB"))
audax.add_player(Player("Guillermo Ortiz", 33, 74, 32, 75, "CB"))
audax.add_player(Player("Esteban Matus", 24, 73, 62, 68, "FB"))
audax.add_player(Player("Marco Collao", 28, 73, 68, 68, "CM"))
audax.add_player(Player("Emanuel Cecchini", 29, 74, 60, 75, "CDM"))
audax.add_player(Player("Gonzalo Rios", 34, 75, 76, 52, "CAM"))
audax.add_player(Player("Alessandro Riep", 23, 72, 75, 40, "WNG"))
audax.add_player(Player("Ignacio Jeraldino", 30, 75, 78, 35, "ST"))
audax.add_player(Player("Lautaro Palacios", 31, 74, 77, 32, "ST"))

team_repo.save_team(audax)

# O'HIGGINS
ohiggins = Team("OHiggins")

ohiggins.add_player(Player("Nicolas Peranic", 41, 73, 12, 79, "GK"))
ohiggins.add_player(Player("Moises Gonzalez", 26, 73, 35, 75, "CB"))
ohiggins.add_player(Player("Leonel Mosevich", 29, 74, 28, 76, "CB"))
ohiggins.add_player(Player("Juan Fuentes", 31, 74, 55, 76, "CDM"))
ohiggins.add_player(Player("Vicente Fernandez", 27, 73, 62, 69, "FB"))
ohiggins.add_player(Player("Camilo Moya", 28, 74, 60, 74, "CDM"))
ohiggins.add_player(Player("Yerko Leiva", 27, 74, 72, 68, "CM"))
ohiggins.add_player(Player("Martin Sarrafiore", 28, 74, 76, 50, "CAM"))
ohiggins.add_player(Player("Joaquin Tapia", 22, 72, 76, 42, "WNG"))
ohiggins.add_player(Player("Esteban Moreira", 24, 73, 76, 35, "ST"))
ohiggins.add_player(Player("Arnaldo Castillo", 28, 74, 78, 38, "ST"))

team_repo.save_team(ohiggins)

# COBRESAL
cobresal = Team("Cobresal")

cobresal.add_player(Player("Leandro Requena", 38, 74, 12, 79, "GK"))
cobresal.add_player(Player("Guillermo Pacheco", 36, 74, 66, 68, "FB"))
cobresal.add_player(Player("Franco Bechtholdt", 32, 74, 32, 76, "CB"))
cobresal.add_player(Player("Francisco Alarcon", 36, 73, 35, 75, "CB"))
cobresal.add_player(Player("Marcelo Jorquera", 37, 73, 65, 69, "FB"))
cobresal.add_player(Player("Diego Cespedes", 28, 74, 50, 75, "CDM"))
cobresal.add_player(Player("Christopher Mesias", 28, 74, 70, 71, "CM"))
cobresal.add_player(Player("Leonardo Valencia", 35, 76, 78, 45, "CAM"))
cobresal.add_player(Player("Franco Garcia", 28, 74, 78, 40, "WNG"))
cobresal.add_player(Player("Cesar Munder", 26, 75, 79, 42, "WNG"))
cobresal.add_player(Player("Diego Coelho", 31, 75, 78, 35, "ST"))

team_repo.save_team(cobresal)

# HUACHIPATO (Actualizado con la reestructuración completa del 11 titular 2026)
huachipato = Team("Huachipato")

huachipato.add_player(Player("Rodrigo Odriozola", 37, 74, 12, 79, "GK"))
huachipato.add_player(Player("Maximiliano Gutierrez", 23, 73, 64, 68, "FB"))
huachipato.add_player(Player("Claudio Torres", 23, 72, 76, 38, "WNG"))
huachipato.add_player(Player("Renzo Malanca", 23, 74, 30, 76, "CB"))
huachipato.add_player(Player("Rafael Caroca", 36, 74, 45, 75, "CB"))
huachipato.add_player(Player("Claudio Sepulveda", 33, 75, 55, 77, "CDM"))
huachipato.add_player(Player("Lucas Velasquez", 22, 71, 60, 67, "FB"))
huachipato.add_player(Player("Santiago Silva", 21, 73, 70, 68, "CM"))
huachipato.add_player(Player("Ezequiel Cañete", 27, 75, 76, 55, "CAM"))
huachipato.add_player(Player("Maicol Leon", 23, 72, 68, 65, "FB"))
huachipato.add_player(Player("Lionel Altamirano", 33, 76, 80, 35, "ST"))

team_repo.save_team(huachipato)

# ÑUBLENSE
nublense = Team("Nublense")

nublense.add_player(Player("Nicola Perez", 36, 75, 12, 80, "GK"))
nublense.add_player(Player("Osvaldo Bosso", 32, 74, 32, 75, "CB"))
nublense.add_player(Player("Carlos Labrin", 35, 73, 30, 74, "CB"))
nublense.add_player(Player("Jovany Campusano", 33, 74, 64, 70, "FB"))
nublense.add_player(Player("Christopher Medina", 25, 73, 62, 68, "FB"))
nublense.add_player(Player("Lorenzo Reyes", 34, 75, 60, 76, "CDM"))
nublense.add_player(Player("Ivan Rozas", 27, 73, 72, 66, "CM"))
nublense.add_player(Player("Gabriel Graciani", 33, 75, 76, 50, "CAM"))
nublense.add_player(Player("Bayron Oyarzo", 31, 74, 78, 45, "WNG"))
nublense.add_player(Player("Patricio Rubio", 37, 75, 79, 35, "ST"))
nublense.add_player(Player("Ismael Sosa", 39, 74, 77, 38, "WNG"))

team_repo.save_team(nublense)

# DEPORTES LA SERENA
la_serena = Team("Deportes La Serena")

la_serena.add_player(Player("Eryin Sanhueza", 30, 72, 10, 72, "GK"))
la_serena.add_player(Player("Enzo Ferrario", 26, 72, 25, 68, "CB"))
la_serena.add_player(Player("Lucas Alarcon", 26, 73, 28, 69, "CB"))
la_serena.add_player(Player("Raul Osorio", 30, 72, 35, 67, "CB"))
la_serena.add_player(Player("Diego Sanhueza", 24, 71, 50, 64, "FB"))
la_serena.add_player(Player("Sebastian Diaz", 29, 72, 52, 68, "CM"))
la_serena.add_player(Player("Sebastián Gallegos", 34, 73, 70, 42, "CAM"))
la_serena.add_player(Player("Ethan Espinoza", 25, 72, 66, 62, "CM"))
la_serena.add_player(Player("Juan Sanchez Sotelo", 38, 73, 74, 30, "ST"))
la_serena.add_player(Player("Alvaro Delgado", 31, 71, 72, 35, "WNG"))
la_serena.add_player(Player("Carlos Lobos", 29, 72, 68, 60, "CM"))

team_repo.save_team(la_serena)

# DEPORTES LIMACHE
limache = Team("Deportes Limache")

limache.add_player(Player("Milton Alvarez", 36, 73, 10, 73, "GK"))
limache.add_player(Player("Rodrigo Moreira", 29, 72, 28, 68, "CB"))
limache.add_player(Player("Gonzalo Paz", 33, 72, 25, 67, "CB"))
limache.add_player(Player("Francisco Silva", 32, 71, 50, 66, "CDM"))
limache.add_player(Player("Felipe Fritz", 28, 72, 64, 55, "FB"))
limache.add_player(Player("Alvaro Cesped", 34, 71, 65, 60, "CM"))
limache.add_player(Player("Luis Cabrera", 32, 71, 52, 65, "CDM"))
limache.add_player(Player("Facundo Juarez", 32, 72, 72, 38, "WNG"))
limache.add_player(Player("Daniel Castro", 32, 73, 74, 32, "WNG"))
limache.add_player(Player("Nelson Da Silva", 30, 72, 73, 30, "ST"))
limache.add_player(Player("Brenno", 26, 71, 10, 71, "CB"))

team_repo.save_team(limache)

# UNIÓN LA CALERA
la_calera = Team("Union La Calera")

la_calera.add_player(Player("Matias Ibañez", 39, 73, 12, 76, "GK"))
la_calera.add_player(Player("Enzo Ferrario", 26, 72, 28, 70, "CB"))
la_calera.add_player(Player("Ezequiel Parnisari", 36, 73, 32, 72, "CB"))
la_calera.add_player(Player("Nahuel Brunet", 25, 72, 28, 71, "CB"))
la_calera.add_player(Player("Diego Ulloa", 23, 72, 58, 66, "FB"))
la_calera.add_player(Player("Esteban Valencia", 26, 72, 68, 64, "CM"))
la_calera.add_player(Player("Matias Cavalleri", 28, 73, 74, 42, "WNG"))
la_calera.add_player(Player("Pablo Parra", 31, 74, 75, 45, "CAM"))
la_calera.add_player(Player("Walter Bou", 32, 75, 77, 35, "ST"))
la_calera.add_player(Player("Franco Soldano", 31, 73, 75, 38, "ST"))
la_calera.add_player(Player("Emmanuel Gigliotti", 39, 73, 75, 35, "ST"))

team_repo.save_team(la_calera)

# UNIVERSIDAD DE CONCEPCIÓN (UDEC) - ASCENDIDO 2026
udec = Team("UDEC")

udec.add_player(Player("Diego Garcia", 26, 72, 25, 69, "CB"))
udec.add_player(Player("Javier Saldias", 24, 71, 55, 64, "FB"))
udec.add_player(Player("Henry Sanhueza", 30, 72, 28, 68, "CB"))
udec.add_player(Player("Esteban Flores", 33, 70, 50, 63, "FB"))
udec.add_player(Player("Camilo Rodriguez", 31, 71, 58, 65, "FB"))
udec.add_player(Player("Kevin Medel", 30, 73, 55, 69, "CDM"))
udec.add_player(Player("Renato Cordero", 23, 73, 58, 70, "CM"))
udec.add_player(Player("Brahian Aleman", 36, 74, 74, 45, "CAM"))
udec.add_player(Player("Reiner Castro", 32, 73, 74, 38, "WNG"))
udec.add_player(Player("Matias Donoso", 39, 72, 75, 32, "ST"))
udec.add_player(Player("Jeison Fuentealba", 23, 72, 70, 60, "CAM"))

team_repo.save_team(udec)

# DEPORTES CONCEPCIÓN - ASCENDIDO 2026
deportes_concepcion = Team("Deportes Concepcion")

deportes_concepcion.add_player(Player("Joaquin Muñoz", 35, 72, 10, 70, "GK"))
deportes_concepcion.add_player(Player("Lautaro Rigazzi", 28, 71, 25, 65, "CB"))
deportes_concepcion.add_player(Player("Sebastian Silva", 34, 71, 28, 66, "CB"))
deportes_concepcion.add_player(Player("Carlos Santibañez", 25, 70, 50, 62, "FB"))
deportes_concepcion.add_player(Player("Felipe Yañez", 21, 71, 55, 63, "FB"))
deportes_concepcion.add_player(Player("Fabrizio Manzo", 23, 71, 65, 58, "CM"))
deportes_concepcion.add_player(Player("Mauro Lopes", 28, 72, 72, 35, "WNG"))
deportes_concepcion.add_player(Player("Benjamin Rivera", 27, 71, 52, 64, "CDM"))
deportes_concepcion.add_player(Player("Ignacio Mesias", 25, 73, 74, 28, "ST"))
deportes_concepcion.add_player(Player("Carlos Escobar", 36, 72, 73, 30, "ST"))
deportes_concepcion.add_player(Player("Gabriel Vargas", 42, 70, 72, 25, "ST"))

team_repo.save_team(deportes_concepcion)