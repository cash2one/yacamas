var uiInit ={
   $win : $(window),
   $nav : $('div#nav'),
   $subNav : $('div#nav li ul'),
   $footer : $('div#footer'),
   $bgAllWrapper : $('div#bg-wrapper'),
   $bgAllImg : $('img#bg-all'),
   $main : $('div#main'),
   $footerMdl : $('div#footer .mdl'),
   $footerLft : $('div#footer .lft'),
   $footerRgt : $('div#footer .rgt'),

  _init: function(){
      this.footer.init();
      this.bgall.init();
  },

  init: function(){
    var topObj = this;
    this._init();
    this.nav.init();
    this.$win.on('resize', function(){
      topObj._init();
      topObj.nav.init();
      /** nav first li english poisiton bug **/
      //$('div#nav>ul>li:first-child').css({'line-height':'21px'});
    }).on('scroll', function(){
      topObj._init();
    });
    this.textScroll.scroll();
    this.erweima.init();
  }
}
/**  nav && subnav **/

uiInit.nav = {
    $sub : uiInit.$subNav,
    $nav : uiInit.$nav,
    posIt : function(obj){
      var thisLft = obj.position().left,
          thisW  = obj.outerWidth(true),
          childUl = obj.children('ul'),
          parentLft = obj.parent().position().left,
          childUlw = childUl.outerWidth(),
          _left = thisLft - thisW; 
          // FIXIT: childUlw is not static
      childUl.html(thisW + '--------------'+ childUl.children('li').width()+'------------------------***:' + thisLft);
      if(_left < parentLft){
        childUl.css('left', parentLft).show();
      }else{
        childUl.css('left', _left).show();
        childUlw = childUl.outerWidth();
         _left = thisLft - childUlw + thisW - 20; 
        if(_left < parentLft){
          childUl.css('left', parentLft).show();
        }else{
          childUl.css('left', _left);
        }
        //  alert(childUl.outerWidth(true));
      }
    },
    init : function(){
      var oNav = this,
          $crntLi = $('#nav li').find('a[if-crnt=1]').parent();
      oNav.posIt($crntLi);
      this.$nav.on('mouseenter', 'li', function(){
        $crntLi.children('ul').hide();
        oNav.posIt($(this));
      }).on('mouseleave', 'li', function(){
        if ($(this).parent().parent().attr('id') == 'nav'){
          oNav.posIt($crntLi);
        }
      });
    
    }
  
}
/**  footer init **/
uiInit.footer = {
  footerH : uiInit.$footer.outerHeight(),
  init : function(){
    var winH = uiInit.$win.innerHeight(),
        winW = uiInit.$win.innerWidth(),
        mainBtm = uiInit.$main.position().top + 
                  uiInit.$main.outerHeight(),
        footerMinW = parseInt(uiInit.$footer.css('min-width')),
        footerTop = winH - this.footerH;

    if(winW <= footerMinW){
      uiInit.$footerMdl.outerWidth(footerMinW 
                                  - uiInit.$footerLft.outerWidth() 
                                  - uiInit.$footerRgt.outerWidth());
    }else{
      uiInit.$footerMdl.outerWidth(winW 
                                  - uiInit.$footerLft.outerWidth() 
                                  - uiInit.$footerRgt.outerWidth());
    }
    if (footerTop < mainBtm + 20){
      footerTop = mainBtm + 20;
    }
    uiInit.$footer.css({'position':'absolute', 'left':'0px', 'top':footerTop});
  }
}

/** bg all **/
uiInit.bgall = {
   $win : uiInit.$win,
   $wrapper : uiInit.$bgAllWrapper,
   $img : uiInit.$bgAllImg,
   init : function(){
     var oImg = new Image(),
         winH = this.$win.innerHeight(),
         winW = this.$win.innerWidth(),
         oBgall = this;
     oImg.src = this.$img.attr('src');
     $(oImg).on('load', function(){ 
       var bgImgW = oImg.width,
           bgImgH = oImg.height,
           scale  = bgImgW / bgImgH,
           wrapperScale = winW / winH;
       oBgall.$wrapper.innerHeight(winH);
       oBgall.$wrapper.innerWidth(winW);
       if (wrapperScale > scale){
          oBgall.$img.outerWidth(oBgall.$wrapper.innerWidth());
          oBgall.$img.outerHeight(oBgall.$wrapper.innerWidth() / scale);
       }else{
          oBgall.$img.outerHeight(oBgall.$wrapper.innerHeight());
          oBgall.$img.outerWidth(oBgall.$wrapper.innerHeight() * scale);
       }
     });
   }
}

/** text scroll **/
uiInit.textScroll = {

  $narrowUp : $('span.up.scroll-nrw'),
  $narrowDown : $('span.down.scroll-nrw'),
  step : 5 * parseInt($('span.up').parent().siblings('div.main').children('div.content').css('line-height')),

  scroll : function(){
    var oScroll = this;

    this.$narrowUp.on('click', function(){
      var $wrapper = $(this).parent().siblings('div.main');
      $wrapper.css('position', 'relative');
      var $textBox = $wrapper.children('div.content'),
          wrapperH = $wrapper.innerHeight(),
          contentH = $textBox.outerHeight(),
          crntTop = $textBox.position().top,
          _top =  crntTop - oScroll.step - 5,
          contentBtm = contentH + crntTop;

      /** make content && its parent wrapper position be "relative"*/
      if (contentBtm <= wrapperH){
        return false;
      }
      else{
        $textBox.css({'position':'relative', 'top': _top});
      }
    })
    this.$narrowDown.on('click', function(){
       var $wrapper = $(this).parent().siblings('div.main'),
           $textBox = $wrapper.children('div.content'),
           crntTop = $textBox.position().top,
           _top =  crntTop + oScroll.step + 5;
           
      if (crntTop >= 0){
        $textBox.css({'position':'relative', 'top': '0px'});
      }
      else{
        $textBox.css({'position':'relative', 'top': _top});
      }
    });
    this.$narrowDown.parent().on('selectstart', function(){return false;});
  }
}

/** er wei ma **/
  uiInit.erweima = {
    $footer : $('div#footer'),
    $weixin : $('div#footer .lft div'),
    $weibo  : $('div#footer .rgt div'),
    $wrapper: $('div#erweima'),


    init : function(){
      var oEwm = this;
      this.$weixin.on('mouseenter', function(){
        var _top = oEwm.$footer.position().top -130 ,
            _lft = $(this).position().left + 53;
        oEwm.$wrapper.attr('class', '');
        oEwm.$wrapper.addClass('weixin');
        oEwm.$wrapper.css({'top':_top, 'left':_lft}).show(300);
      }).on('mouseout', function(){
        oEwm.$wrapper.slideUp(500);
      }),

      this.$weibo.on('mouseenter', function(){
        var _top = oEwm.$footer.position().top -160 ,
            _lft = $(this).position().left - 105;
        oEwm.$wrapper.attr('class', '');
        oEwm.$wrapper.addClass('weibo');
        oEwm.$wrapper.css({'top':_top, 'left':_lft}).show(300);
      }).on('mouseout', function(){
        oEwm.$wrapper.slideUp(500);
      })
    }
  }

uiInit.init();

/****** ie 检测 *******/
			function detectBrowser(){	
				var browser=navigator.appName;
				var b_version=navigator.appVersion;
				var version=parseFloat(b_version); 
				// TODO: 检查是ietester 不准还是ie 返回版本就是不准ietester 下 ie6 version = 4 ie7 = 5 。。。 
				if ((browser=="Microsoft Internet Explorer") && (version==6 || version==6 || version==4)){
					bgSrc = $('#bg-all img').attr('src');
					$('#bg-wrapper').remove(); 
					//alert($('#bg-wrapper').height());
					$('body').css({'background': 'url(images/bgbig/11.jpg) fixed'});
				} 
	  		}
			detectBrowser();


