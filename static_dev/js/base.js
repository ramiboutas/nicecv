console.log("Hi I am the nice server")



import Cropper from "https://cdnjs.cloudflare.com/ajax/libs/cropperjs/1.5.12/cropper.min.js";

const image = document.getElementById('image-to-crop');
const cropper = new Cropper(image, {
  aspectRatio: 16 / 9,
  crop(event) {
    console.log(event.detail.x);
    console.log(event.detail.y);
    console.log(event.detail.width);
    console.log(event.detail.height);
    console.log(event.detail.rotate);
    console.log(event.detail.scaleX);
    console.log(event.detail.scaleY);
  },
});
