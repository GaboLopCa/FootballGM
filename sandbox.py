from models.player import Player
from models.team import Team
import services.team_repository as team_repo

# COLO-COLO (Plantel 2026 tras salidas a Europa y nuevos fichajes)
colo_colo = Team("Colo-Colo")

colo_colo.add_player(Player("Fernando de Paul", 35, 77))
colo_colo.add_player(Player("Jeyson Rojas", 24, 74))
colo_colo.add_player(Player("Jonathan Villagra", 25, 76))
colo_colo.add_player(Player("Joaquin Sosa", 24, 76))
colo_colo.add_player(Player("Erick Wiemberg", 31, 76))
colo_colo.add_player(Player("Victor Mendez", 26, 78))
colo_colo.add_player(Player("Tomas Alarcon", 27, 77))
colo_colo.add_player(Player("Arturo Vidal", 39, 81))
colo_colo.add_player(Player("Claudio Aquino", 34, 78))
colo_colo.add_player(Player("Maximiliano Romero", 27, 77))
colo_colo.add_player(Player("Javier Correa", 33, 78))

team_repo.save_team(colo_colo)

# UNIVERSIDAD DE CHILE (Con los retornos estelares y compras definitivas)
u_de_chile = Team("Universidad de Chile")

u_de_chile.add_player(Player("Gabriel Castellon", 32, 78))
u_de_chile.add_player(Player("Fabian Hormazabal", 30, 77))
u_de_chile.add_player(Player("Franco Calderon", 28, 77))
u_de_chile.add_player(Player("Matias Zaldivia", 35, 77))
u_de_chile.add_player(Player("Marcelo Morales", 23, 78))
u_de_chile.add_player(Player("Marcelo Diaz", 39, 76))
u_de_chile.add_player(Player("Charles Aranguiz", 37, 79))
u_de_chile.add_player(Player("Lucas Romero", 23, 75))
u_de_chile.add_player(Player("Javier Altamirano", 26, 78))
u_de_chile.add_player(Player("Eduardo Vargas", 36, 78))
u_de_chile.add_player(Player("Maximiliano Guerrero", 26, 77))

team_repo.save_team(u_de_chile)

# UNIVERSIDAD CATÓLICA (Plantel renovado 2026 dirigido por Daniel Garnero)
u_catolica = Team("Universidad Catolica")

u_catolica.add_player(Player("Vicente Bernedo", 25, 74))
u_catolica.add_player(Player("Bernardo Cerezo", 30, 75))
u_catolica.add_player(Player("Branco Ampuero", 32, 76))
u_catolica.add_player(Player("Daniel Gonzalez", 23, 75))
u_catolica.add_player(Player("Cristian Cuevas", 31, 75))
u_catolica.add_player(Player("Gary Medel", 38, 77))
u_catolica.add_player(Player("Jhojan Valencia", 29, 75))
u_catolica.add_player(Player("Matias Palavecino", 28, 76))
u_catolica.add_player(Player("Clemente Montes", 25, 75))
u_catolica.add_player(Player("Justo Giani", 27, 74))
u_catolica.add_player(Player("Fernando Zampedri", 38, 81))

team_repo.save_team(u_catolica)

# PALESTINO
palestino = Team("Palestino")

palestino.add_player(Player("Cesar Rigamonti", 38, 76))
palestino.add_player(Player("Benjamin Rojas", 25, 74))
palestino.add_player(Player("Cristian Suarez", 39, 74))
palestino.add_player(Player("Ivan Roman", 19, 75))
palestino.add_player(Player("Dilan Zuñiga", 30, 74))
palestino.add_player(Player("Ariel Martinez", 32, 74))
palestino.add_player(Player("Misael Davila", 35, 75))
palestino.add_player(Player("Joe Abrigo", 31, 75))
palestino.add_player(Player("Bryan Carrasco", 35, 75))
palestino.add_player(Player("Junior Marabel", 28, 74))
palestino.add_player(Player("Gonzalo Sosa", 37, 75))

team_repo.save_team(palestino)

# COQUIMBO UNIDO
coquimbo = Team("Coquimbo Unido")

coquimbo.add_player(Player("Diego Sanchez", 39, 75))
coquimbo.add_player(Player("Dylan Escobar", 25, 74))
coquimbo.add_player(Player("Bruno Cabrera", 29, 74))
coquimbo.add_player(Player("Manuel Fernandez", 37, 73))
coquimbo.add_player(Player("Sebastian Cabrera", 28, 74))
coquimbo.add_player(Player("Alejandro Camargo", 37, 75))
coquimbo.add_player(Player("Dylan Glaby", 29, 76))
coquimbo.add_player(Player("Juan Manuel Vazquez", 31, 74))
coquimbo.add_player(Player("Cristian Zavala", 26, 76))
coquimbo.add_player(Player("Andres Chavez", 35, 74))
coquimbo.add_player(Player("Jonatan Bauman", 35, 74))

team_repo.save_team(coquimbo)

# EVERTON
everton = Team("Everton")

everton.add_player(Player("Ignacio Gonzalez", 36, 75))
everton.add_player(Player("Felipe Campos", 32, 74))
everton.add_player(Player("Diego Oyarzun", 33, 74))
everton.add_player(Player("Eduardo Bauermann", 30, 76))
everton.add_player(Player("Alex Ibacache", 27, 75))
everton.add_player(Player("Alvaro Madrid", 31, 76))
everton.add_player(Player("Benjamin Berrios", 28, 75))
everton.add_player(Player("Federico Martinez", 30, 75))
everton.add_player(Player("Rodrigo Contreras", 30, 77))
everton.add_player(Player("Kevin Mendez", 30, 74))
everton.add_player(Player("Lautaro Pastran", 24, 75))

team_repo.save_team(everton)

# AUDAX ITALIANO
audax = Team("Audax Italiano")

audax.add_player(Player("Tomas Ahumada", 24, 74))
audax.add_player(Player("Nicolas Fernandez", 27, 74))
audax.add_player(Player("German Guiffrey", 28, 74))
audax.add_player(Player("Guillermo Ortiz", 33, 74))
audax.add_player(Player("Esteban Matus", 24, 73))
audax.add_player(Player("Marco Collao", 28, 73))
audax.add_player(Player("Emanuel Cecchini", 29, 74))
audax.add_player(Player("Gonzalo Rios", 34, 75))
audax.add_player(Player("Alessandro Riep", 23, 72))
audax.add_player(Player("Ignacio Jeraldino", 30, 75))
audax.add_player(Player("Lautaro Palacios", 31, 74))

team_repo.save_team(audax)

# O'HIGGINS
ohiggins = Team("OHiggins")

ohiggins.add_player(Player("Nicolas Peranic", 41, 73))
ohiggins.add_player(Player("Moises Gonzalez", 26, 73))
ohiggins.add_player(Player("Leonel Mosevich", 29, 74))
ohiggins.add_player(Player("Juan Fuentes", 31, 74))
ohiggins.add_player(Player("Vicente Fernandez", 27, 73))
ohiggins.add_player(Player("Camilo Moya", 28, 74))
ohiggins.add_player(Player("Yerko Leiva", 27, 74))
ohiggins.add_player(Player("Martin Sarrafiore", 28, 74))
ohiggins.add_player(Player("Joaquin Tapia", 22, 72))
ohiggins.add_player(Player("Esteban Moreira", 24, 73))
ohiggins.add_player(Player("Arnaldo Castillo", 28, 74))

team_repo.save_team(ohiggins)

# COBRESAL
cobresal = Team("Cobresal")

cobresal.add_player(Player("Leandro Requena", 38, 74))
cobresal.add_player(Player("Guillermo Pacheco", 36, 74))
cobresal.add_player(Player("Franco Bechtholdt", 32, 74))
cobresal.add_player(Player("Francisco Alarcon", 36, 73))
cobresal.add_player(Player("Marcelo Jorquera", 37, 73))
cobresal.add_player(Player("Diego Cespedes", 28, 74))
cobresal.add_player(Player("Christopher Mesias", 28, 74))
cobresal.add_player(Player("Leonardo Valencia", 35, 76))
cobresal.add_player(Player("Franco Garcia", 28, 74))
cobresal.add_player(Player("Cesar Munder", 26, 75))
cobresal.add_player(Player("Diego Coelho", 31, 75))

team_repo.save_team(cobresal)

# HUACHIPATO (Actualizado con la reestructuración completa del 11 titular 2026)
huachipato = Team("Huachipato")

huachipato.add_player(Player("Rodrigo Odriozola", 37, 74))
huachipato.add_player(Player("Maximiliano Gutierrez", 23, 73))
huachipato.add_player(Player("Claudio Torres", 23, 72))
huachipato.add_player(Player("Renzo Malanca", 23, 74))
huachipato.add_player(Player("Rafael Caroca", 36, 74))
huachipato.add_player(Player("Claudio Sepulveda", 33, 75))
huachipato.add_player(Player("Lucas Velasquez", 22, 71))
huachipato.add_player(Player("Santiago Silva", 21, 73))
huachipato.add_player(Player("Ezequiel Cañete", 27, 75))
huachipato.add_player(Player("Maicol Leon", 23, 72))
huachipato.add_player(Player("Lionel Altamirano", 33, 76))

team_repo.save_team(huachipato)

# ÑUBLENSE
nublense = Team("Nublense")

nublense.add_player(Player("Nicola Perez", 36, 75))
nublense.add_player(Player("Osvaldo Bosso", 32, 74))
nublense.add_player(Player("Carlos Labrin", 35, 73))
nublense.add_player(Player("Jovany Campusano", 33, 74))
nublense.add_player(Player("Christopher Medina", 25, 73))
nublense.add_player(Player("Lorenzo Reyes", 34, 75))
nublense.add_player(Player("Ivan Rozas", 27, 73))
nublense.add_player(Player("Gabriel Graciani", 33, 75))
nublense.add_player(Player("Bayron Oyarzo", 31, 74))
nublense.add_player(Player("Patricio Rubio", 37, 75))
nublense.add_player(Player("Ismael Sosa", 39, 74))

team_repo.save_team(nublense)

# DEPORTES LA SERENA
la_serena = Team("Deportes La Serena")

la_serena.add_player(Player("Eryin Sanhueza", 30, 72))
la_serena.add_player(Player("Enzo Ferrario", 26, 72))
la_serena.add_player(Player("Lucas Alarcon", 26, 73))
la_serena.add_player(Player("Raul Osorio", 30, 72))
la_serena.add_player(Player("Diego Sanhueza", 24, 71))
la_serena.add_player(Player("Sebastian Diaz", 29, 72))
la_serena.add_player(Player("Sebastián Gallegos", 34, 73))
la_serena.add_player(Player("Ethan Espinoza", 25, 72))
la_serena.add_player(Player("Juan Sanchez Sotelo", 38, 73))
la_serena.add_player(Player("Alvaro Delgado", 31, 71))
la_serena.add_player(Player("Carlos Lobos", 29, 72))

team_repo.save_team(la_serena)

# DEPORTES LIMACHE
limache = Team("Deportes Limache")

limache.add_player(Player("Milton Alvarez", 36, 73))
limache.add_player(Player("Rodrigo Moreira", 29, 72))
limache.add_player(Player("Gonzalo Paz", 33, 72))
limache.add_player(Player("Francisco Silva", 32, 71))
limache.add_player(Player("Felipe Fritz", 28, 72))
limache.add_player(Player("Alvaro Cesped", 34, 71))
limache.add_player(Player("Luis Cabrera", 32, 71))
limache.add_player(Player("Facundo Juarez", 32, 72))
limache.add_player(Player("Daniel Castro", 32, 73))
limache.add_player(Player("Nelson Da Silva", 30, 72))
limache.add_player(Player("Brenno", 26, 71))

team_repo.save_team(limache)

# UNIÓN LA CALERA
la_calera = Team("Union La Calera")

la_calera.add_player(Player("Matias Ibañez", 39, 73))
la_calera.add_player(Player("Enzo Ferrario", 26, 72))
la_calera.add_player(Player("Ezequiel Parnisari", 36, 73))
la_calera.add_player(Player("Nahuel Brunet", 25, 72))
la_calera.add_player(Player("Diego Ulloa", 23, 72))
la_calera.add_player(Player("Esteban Valencia", 26, 72))
la_calera.add_player(Player("Matias Cavalleri", 28, 73))
la_calera.add_player(Player("Pablo Parra", 31, 74))
la_calera.add_player(Player("Walter Bou", 32, 75))
la_calera.add_player(Player("Franco Soldano", 31, 73))
la_calera.add_player(Player("Emmanuel Gigliotti", 39, 73))

team_repo.save_team(la_calera)

# UNIVERSIDAD DE CONCEPCIÓN (UDEC) - ASCENDIDO 2026
udec = Team("UDEC")

udec.add_player(Player("Diego Garcia", 26, 72))
udec.add_player(Player("Javier Saldias", 24, 71))
udec.add_player(Player("Henry Sanhueza", 30, 72))
udec.add_player(Player("Esteban Flores", 33, 70))
udec.add_player(Player("Camilo Rodriguez", 31, 71))
udec.add_player(Player("Kevin Medel", 30, 73))
udec.add_player(Player("Renato Cordero", 23, 73))
udec.add_player(Player("Brahian Aleman", 36, 74))
udec.add_player(Player("Reiner Castro", 32, 73))
udec.add_player(Player("Matias Donoso", 39, 72))
udec.add_player(Player("Jeison Fuentealba", 23, 72))

team_repo.save_team(udec)

# DEPORTES CONCEPCIÓN - ASCENDIDO 2026
deportes_concepcion = Team("Deportes Concepcion")

deportes_concepcion.add_player(Player("Joaquin Muñoz", 35, 72))
deportes_concepcion.add_player(Player("Lautaro Rigazzi", 28, 71))
deportes_concepcion.add_player(Player("Sebastian Silva", 34, 71))
deportes_concepcion.add_player(Player("Carlos Santibañez", 25, 70))
deportes_concepcion.add_player(Player("Felipe Yañez", 21, 71))
deportes_concepcion.add_player(Player("Fabrizio Manzo", 23, 71))
deportes_concepcion.add_player(Player("Mauro Lopes", 28, 72))
deportes_concepcion.add_player(Player("Benjamin Rivera", 27, 71))
deportes_concepcion.add_player(Player("Ignacio Mesias", 25, 73))
deportes_concepcion.add_player(Player("Carlos Escobar", 36, 72))
deportes_concepcion.add_player(Player("Gabriel Vargas", 42, 70))

team_repo.save_team(deportes_concepcion)