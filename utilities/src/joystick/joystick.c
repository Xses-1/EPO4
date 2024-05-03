#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <linux/joystick.h>

int main (void) {
	int js;
	int axis[2];
	struct js_event event;

	js = open("/dev/input/js3",	O_RDONLY);
	
	if (js == -1) {
		perror("Could not open the joystick!");
		return 0;
	}

	// This is a very dumb way of initializing stuff but whatever
	axis[0] = 0;
	axis[1] = 0;

	while (read(js, &event, sizeof(event)) == sizeof(event)) {
		if (event.type == JS_EVENT_AXIS) {
			switch (event.number) {
				case 0:
					axis[0] = event.value;
					break;

				case 3:
					axis[1] = event.value;
					break;

				default:
					break;
			}
		}

		fflush(stdout);

		axis[0] = axis[0] * -50 / 32767 + 150;
		axis[1] = axis[1] * -15 / 32767 + 150;

		printf("%d00%d\n", axis[0], axis[1]);
	}

	close(js);

	return 0;
}
