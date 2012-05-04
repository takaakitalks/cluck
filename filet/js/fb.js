/**
 * A library to handle Facebook data in Galleriffic
 *
 * Copyright (c) 2012 CLUCK
 * Licensed under the MIT License:
 *   http://www.opensource.org/licenses/mit-license.php
 *
 */

var FBImage = function() {
    this.thumbnailUrl;
    this.imgUrl;
    this.message;
    this.userImg;
}

FBImage.prototype.setImgFromData = function(fb_data) {
  if(fb_data.picture) {
    this.thumbnailUrl = fb_data.picture;
    this.imgUrl = fb_data.picture.replace(/_s\.(jpg|gif|png)$/g,'_n\.$1');
    this.message = fb_data.message;
    this.userImg = 'http://graph.facebook.com/' + fb_data.from.id + '/picture';
    this.userName = fb_data.from.name;
  }
}

var DataManager = function() {
  this.images = [];
}

DataManager.prototype.parse = function(fb_all_data) {
  var dm = this;
  $(fb_all_data).each(function(idx, fb_data) {
      var img = new FBImage();
      if (fb_data.picture) {
        img.setImgFromData(fb_data);
        dm.images.push(img);
      }
  });
}

DataManager.prototype.createList = function() {
  if (this.images.length) {
    $(this.images).each(function(idx, img) {
        var li = $('<li></li>');
        var a = $('<a></a>').attr({
          class: 'thumb',
          href: img.imgUrl
        });
        var thumbImg = $('<img />').attr({
          src: img.thumbnailUrl,
          height: '50px'
        });
        var capDiv = $('<div></div>').attr({
          class: 'caption'
        });
        var descDiv = $('<div></div>').attr({
          class: 'image-desc'
        }) .html('<span>' + img.message + '</span>');
        var userNameDiv = $('<div></div>').attr({
          class: 'user-name',
          }) .html('<span>posted by &nbsp;' + img.userName + '</span>');
        var userImg = $('<img />').attr({
          class: 'user-profile-img',
          src: img.userImg
          });

        capDiv.append(userImg, descDiv, userNameDiv);
        li.append(a.append(thumbImg), capDiv);
        $('.thumbs').append(li);
      });
    }
}

