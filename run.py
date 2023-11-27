import flight_getter as flg
import inky_updater as inu
import time

inky = None
setup_done = False

next_fl = None
curr_time = None

log_path = "/home/pi/coding/python_scripts/flight_service/flight_service.log"
log = None

next_check_time = None

def append_to_log(msg):
	global log
	log = open(log_path, "a")
	log.write(msg + '\n')
	log.close()


def get_check_time(flight: dict) -> str:
	if flight["status"].find("EST") != -1:
		time = flight["status"][len(flight["status"])-5:]
	else:
		time = flight["time"]
	global curr_time
	if time < curr_time:
		time = offset_time(curr_time, 0, 1)
	return time

full_time_format = "%d %b - %T"

def startup_setup():
	global inky
	inky = inu.setup_inky()
	global curr_time
	curr_time = time.strftime("%H:%M", time.localtime())
	global next_fl
	next_fl = flg.get_next_flight()
	global next_check_time
	next_check_time = offset_time(get_check_time(next_fl), 0, -5)
	append_to_log("Started setup at: " + time.strftime(full_time_format, time.localtime()))
	inu.update_inky(next_fl, inky)
	append_to_log("Updated inky at:  " + time.strftime(full_time_format, time.localtime()) + " with flight: " + next_fl["fl_no"] + "-" + next_fl["origin"] + "-" + next_fl["status"])
	append_to_log("Checking next at: " + time.strftime("%d %b - " + next_check_time + ":00"))
	global setup_done
	setup_done = True


def offset_time(time: str, hoff:int, moff:int) -> str:
	h = int(time[0:2])
	m = int(time[3:])
	newm = (m + moff) % 60
	newh = (h + int((m + moff) / 60) + hoff) % 24
	if moff < 0 and moff + m < 0:
		newh -= 1
	sh = f'{newh:02d}'
	sm = f'{newm:02d}'
	res = sh + ':' + sm
	return res

def update():
	new_fl = flg.get_next_flight()
	append_to_log("Checked for flight at: " + time.strftime(full_time_format, time.localtime()))
	global next_fl
	global inky
	global next_check_time
	if new_fl != next_fl:
		next_fl = new_fl
		inu.update_inky(next_fl, inky)
		append_to_log("Updated inky at:  " + time.strftime(full_time_format, time.localtime()) + " with flight: " + next_fl["fl_no"] + "-" + next_fl["origin"] + "-" + next_fl["status"])
		next_check_time = offset_time(get_check_time(next_fl), 0, -5)
	else:
		next_check_time = offset_time(next_check_time, 0, 1)
	append_to_log("Checking next at: " + time.strftime("%d %b - " + next_check_time + ":00"))


while True:
	if not setup_done:
		startup_setup()
	curr_time = time.strftime("%H:%M", time.localtime())
	if curr_time == next_check_time:
		update()
