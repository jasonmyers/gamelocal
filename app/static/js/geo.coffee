
LOCATED = 'located'

valid_position = (latitude, longitude) ->
    return -90 <= latitude <= 90 and -180 <= longitude <= 180

$ ->
    $('#map').each ->

        defaultLatitude = parseFloat($(this).data('defaultLatitude'))
        defaultLongitude = parseFloat($(this).data('defaultLongitude'))

        map = L.map('map').setView([0, 0], 2)

        if valid_position(defaultLatitude, defaultLongitude)
            map.setView([defaultLatitude, defaultLongitude], 12)

        L.tileLayer 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        .addTo(map)

        L.control.locate
            position: 'topright'
            drawCircle: false
            icon: 'icon-direction'
            onLocationError: (err) ->
            onLocationOutsideMapBounds: (context) ->
            locateOptions:
                maxZoom: 12

        .addTo(map)

        map.on 'moveend', (e) ->
            loadClubs map

        loadClubs map

        map.on 'locationfound', (e) ->
            # Found location via browser
            if $.jStorage.storageAvailable()
                if $.jStorage.get(LOCATED) is null
                    $.post '/users/locate',
                        latitude: e.latitude
                        longitude: e.longitude

                    $.jStorage.set(LOCATED, true)

        map.on 'locationerror', (e) ->
            # Couldn't find location via browser
            if $.jStorage.storageAvailable()
                $.jStorage.set(LOCATED, false)


loadClubs = (map) ->
    southwest = map.getBounds().getSouthWest()
    northeast = map.getBounds().getNorthEast()
    $.get '/clubs/map',
        southwest: "#{southwest.lat},#{southwest.lng}"
        northeast: "#{northeast.lat},#{northeast.lng}"
    .done (data) ->
        for club in data.clubs or []
            L.marker([club.latitude, club.longitude])
                .addTo(map)
                .bindLabel("#{club.name}")  # Hover
                .bindPopup("
                    #{club.name} | <a href='#{club.url}'>Details</a>
                    <br/>
                    #{club.full_address}"
                )  # Click
    .fail (x, s, e) ->
        alert 'There was a problem loading the map data'
