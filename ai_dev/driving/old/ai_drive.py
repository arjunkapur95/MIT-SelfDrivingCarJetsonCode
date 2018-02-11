import capture.py
import classify.py

model_filename="models/30epoch_depthrgb.hdf5"
throttle=0.0
image_size=250

while 1:
	#get image from camera
	img=capture.capture_image(image_size)
	steering_val = classify.evaluate_one(img,model_filename)

	print('throttle\t{0:.4f}\t{1:.4f}'.format(throttle,steering_val))
	# move(throttle,steering_val)