$(function(){
window.FormView = Backbone.View.extend({
    el: $("#search_form"),
    search_ads: function(e){
        e.preventDefault();
        $.getJSON("http://localhost:8000/api/v1/ad/?format=json",{}, function(data){
            var meta = data.meta;
            var objects = data.objects;

            for (var i in objects){
                console.log(objects[i].title);
                var ad = new window.Ad(objects[i]);
                var adView = new window.AdView({model: ad});
                adView.render();

            }
        });

    },
    events: {
        "submit": "search_ads"
    }

});
window.AdView = Backbone.View.extend({
    render: function(){
        var ad = _.template($("#ad_template").html(), this.model.toJSON());
        $("#ads").append(ad);
    }
});

    var formview = new window.FormView;

});
