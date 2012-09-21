(function($) {
    
    $.fn.shippingFreight = function(customOptions) {  //Add the function
        var options = $.extend({}, $.fn.shippingFreight.defaultOptions, customOptions);
        return this.each(function() { //Loop over each element in the set and return them to keep the chain alive.
            var $this = $(this);
            
            $countries = $this.find("select[name='country']");
            $states = $this.find("select[name='state']");

            $countries.unbind().on('change', function(e){
                $states.html('<option value="-1">carregando...</option>');
                $.ajax({
                    url: options.urls.states.replace('{country}', $countries.val()),
                    method: 'GET',
                    success: function(response){

                        console.log('response', response);
                        $states.html('');

                        $.each(response.states, function(){
                            console.log('state', this);
                            $states.append('<option value="'+ this.id +'">'+ this.name +'</option>');
                        });

                        if (response.states.length == 0){
                            $states.html('<option value="-1">nenhum estado encontrado</option>');
                        }
                        
                    }
                });
            });

            $countries.trigger('change');
        });
    };
 
    $.fn.shippingFreight.defaultOptions = {
        currency : "R$",
        urls: {
            states: '/shipping/countries/{country}.json'
        }
    };
})(jQuery);