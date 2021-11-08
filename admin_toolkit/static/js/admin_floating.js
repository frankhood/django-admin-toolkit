!function($){
    $(document).ready(function(){
        var $clf=$('#changelist-filter');
        if($clf.length){
            $('#changelist').removeClass("filtered");
            $('#changelist-filter').
                wrapInner('<div class="filter-container"></div>').
                prepend('<a href="" class="label-click">Filtra</a>');
            $('#changelist-filter').tabSlideOut({
                tabHandle: '.label-click',                     //class of the element that will become your tab
                pathToTabImage: window.extraContext.djangoAdminToolkit.filterFloatingImageUrl, //path to the image for the tab //Optionally can be set using css
                imageHeight: '50px',                     //height of tab image           //Optionally can be set using css
                imageWidth: '30px',                       //width of tab image            //Optionally can be set using css
                tabLocation: 'right',                      //side of screen where tab lives, top, right, bottom, or left
                speed: 300,                               //speed of animation
                action: 'click',                          //options: 'click' or 'hover', action to trigger animation
                topPos: '50px',                          //position from the top/ use if tabLocation is left or right
                //leftPos: '20px',                          //position from left/ use if tabLocation is bottom or top
                fixedPosition: true                      //options: true makes it stick(fixed position) on scroll
            });
            
            var chagelistOffset= parseInt($('#changelist').offset().top );
            $(document).scroll(function(evt){
                var scrollpos = (document.documentElement.scrollTop || document.body.scrollTop);
                if (scrollpos > chagelistOffset) { /* blocca */
                    $('#changelist-filter').addClass('upper-fixed')
                } else { /* scrolla */
                    $('#changelist-filter').removeClass('upper-fixed');
                }
            });
        }
    });
}(window.django.jQuery||window.jQuery);
