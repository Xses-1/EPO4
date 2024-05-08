#include <stdio.h>
#include <stdbool.h>

#include <fcntl.h>
#include <unistd.h>
#include <linux/joystick.h>
#include <linux/uinput.h>
#include <sys/select.h>

int main (void) {
	bool update0, update1;
	int js;
	int axis[2];

	struct js_event event;
	struct timeval timeout;
	fd_set set;

	timeout.tv_sec = 0;
	timeout.tv_usec = 10;

	js = open("/dev/input/js3",	O_RDONLY);
	
	if (js == -1) {
		perror("Could not open the joystick!");
		return 0;
	}

	// This is a very dumb way of initializing stuff but whatever
	axis[0] = 150;
	axis[1] = 150;

	while (1) {

		FD_ZERO(&set);
		FD_SET(js, &set);
		int rv = select(js + 1, &set, NULL, NULL, &timeout);

		if (rv == -1) {
			perror("Select 1 broky!");

		} else if (rv != 0) {
			if (read(js, &event, sizeof(event)) != sizeof(event)) {
				perror("End of the input stream!");
				close(js);
				return 0;       
			}
		}

		update0 = 0;
		update1 = 0;

		if (event.type == JS_EVENT_AXIS) {
			switch (event.number) {
				case 0:
					axis[0] = event.value;
					update0 = 1;
					break;

				case 3:
					axis[1] = event.value;
					update1 = 1;
					break;

				default:
					break;
			}
		}

		fflush(stdout);

		if (update0 == 1) {
			axis[0] = axis[0] * -50 / 32767 + 150;
			update0 = 0;
		}

		if (update1 == 1) {
			axis[1] = axis[1] * -15 / 32767 + 150;
			update1 = 0;
		}

		printf("%d00%d\n", axis[0], axis[1]);

		usleep(100);
	}

	close(js);

	return 0;
}
