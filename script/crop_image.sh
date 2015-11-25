composite -compose CopyOpacity ../media/masks/5masks/mask5.png ../media/campaign/flower.jpg ../media/campaign/center.png
convert ../media/campaign/center.png  -gravity Center  -crop 200x200+0+0 +repage  ../media/campaign/center.png
composite -compose CopyOpacity ../media/masks/5masks/mask3.png ../media/campaign/flower.jpg ../media/campaign/north.png
convert ../media/campaign/north.png  -gravity north  -crop 600x150+0+0 +repage  ../media/campaign/north.png
composite -compose CopyOpacity ../media/masks/5masks/mask1.png ../media/campaign/flower.jpg ../media/campaign/west.png
convert ../media/campaign/west.png  -gravity west  -crop 260x400+0+0 +repage  ../media/campaign/west.png
composite -compose CopyOpacity ../media/masks/5masks/mask2.png ../media/campaign/flower.jpg ../media/campaign/south.png
convert ../media/campaign/south.png  -gravity south  -crop 600x160+0+0 +repage  ../media/campaign/south.png
composite -compose CopyOpacity ../media/masks/5masks/mask4.png ../media/campaign/flower.jpg ../media/campaign/east.png
convert ../media/campaign/east.png  -gravity east  -crop 260x400+0+0 +repage  ../media/campaign/east.png
