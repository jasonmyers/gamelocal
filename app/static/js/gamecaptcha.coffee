class Piece
    constructor: (glyph, color) ->
        @glyph = glyph
        @color = color

    display: (cls) =>
        $("<span class='piece #{@color} #{cls}'>#{@glyph}</span>")

renderers =
    go: ($boardContainer, boardCode) ->
        game = "go"
        boardSize = 9

        $boardContainer.html('')
        $board = $("<div id='gameCaptchaBoard' class='gameCaptchaBoard #{game}CaptchaBoard'>")
        $board.appendTo $boardContainer

        pieces =
            # White stone
            "\u25cb": new Piece("\u25cf", "light")
            # Black stone
            "\u25cf": new Piece("\u25cf", "dark")

        mover = pieces["\u25cf"]

        console.log boardCode
        console.log mover

        x = 0
        y = 0
        for space in boardCode
            if space is "|"
                x = 0
                y = y +  1
                continue

            $square = $("<span class='square light'>")
            $square.data('x', x)
            $square.data('y', y)

            if space isnt '_'
                pieces[space].display('staticPiece').appendTo $square

            $square.hover ->
                if not $(this).find('span.piece').length
                    mover.display('hoverPiece').appendTo $(this)
            ,
            ->
                $(this).find('span.hoverPiece').remove()

            $square.mouseup ->
                 if not $(this).find('span.staticPiece').length
                     $board.find('span.answerPiece').remove()
                     $(this).find('span.hoverPiece').remove()
                     mover.display('staticPiece answerPiece').appendTo $(this)
                     answer = "#{mover.glyph} #{$(this).data('x')} #{$(this).data('y')}"
                     $("input#gameCaptchaResponse").val(answer)

            # Corners
            if x is 0 and y is 0
                grids = ['topleft']
            else if x is 0 and y is boardSize - 1
                grids = ['bottomleft']
            else if x is boardSize - 1 and y is 0
                grids = ['topright']
            else if x is boardSize - 1 and y is boardSize - 1
                grids = ['bottomright']

            # Sides
            else if y is 0
                grids = ['topright', 'topleft']
            else if y is boardSize - 1
                grids = ['bottomright', 'bottomleft']
            else if x is 0
                grids = ['topleft', 'bottomleft']
            else if x is boardSize - 1
                grids = ['topright', 'bottomright']

            # Inner
            else
                grids = ['bottomright', 'topleft']

            for grid in grids
                $("<span class='grid #{grid}'>").prependTo $square

            $square.appendTo $board
            x = x + 1

    chess: ($boardContainer, boardCode) ->
        game = "chess"

        $boardContainer.html('')
        $board = $("<div id='gameCaptchaBoard' class='gameCaptchaBoard #{game}CaptchaBoard'>")
        $board.appendTo $boardContainer

        pieces =
            # White King
            "\u2654": new Piece("\u265A", "light")
            # Black Queen
            "\u265B": new Piece("\u265B", "dark")
            # Black Rook
            "\u265C": new Piece("\u265C", "dark")
            # Black Bishop
            "\u265D": new Piece("\u265D", "dark")
            # Black Knight
            "\u265E": new Piece("\u265E", "dark")

        for space in boardCode
            if space of pieces and space isnt "\u2654"
                mover = pieces[space]
                break

        x = 0
        y = 0
        square_colors = ['light', 'dark']
        for space in boardCode
            if space is "|"
                x = 0
                y = y + 1
                continue

            color = square_colors[(y % 2) ^ (x % 2)]

            $square = $("<span class='square #{color}'>")
            $square.data('x', x)
            $square.data('y', y)

            if space isnt '_'
                pieces[space].display('staticPiece').appendTo $square

            $square.hover ->
                if not $(this).find('span.piece').length
                    mover.display('hoverPiece').appendTo $(this)
            ,
            ->
                $(this).find('span.hoverPiece').remove()

            $square.mouseup ->
                 if not $(this).find('span.staticPiece').length
                     $board.find('span.answerPiece').remove()
                     $(this).find('span.hoverPiece').remove()
                     mover.display('staticPiece answerPiece').appendTo $(this)
                     answer = "#{mover.glyph} #{$(this).data('x')} #{$(this).data('y')}"
                     $("input#gameCaptchaResponse").val(answer)

            $square.appendTo $board
            x = x + 1

loadBoard = ($gameCaptcha, options) ->
    $boardContainer = $gameCaptcha.find('div#gameCaptchaBoardContainer')

    $gameField = $gameCaptcha.find('#gameCaptchaGame')
    game = $gameField.val()

    $challengeField = $gameCaptcha.find('input#gameCaptchaChallenge')
    boardCode = $challengeField.val()

    if boardCode > ''
        return renderers[game]($boardContainer, boardCode)

    loadError = options?.custom_translations?.load_error or 'Oops, there was a problem loading the board'

    if not game > ''
        gameCaptchaError(loadError)

    $.get "/gamecaptcha/",
        game: game

    .done (response) ->
        boardCode = response?.board_code

        if boardCode > ''
            $challengeField.val(boardCode)
            renderers[game]($boardContainer, boardCode)

        else
            gameCaptchaError(loadError)

    .fail (x, s, e) ->
        gameCaptchaError(loadError)


$ ->
    $("div#gameCaptcha").each ->
        $gameCaptcha = $(this)
        options = window["gameCaptchaOptions"] or {}

        loadBoard($gameCaptcha, options)

        $gameCaptcha.find('button#gameCaptchaRefresh').click ->
            $gameCaptcha.find('input#gameCaptchaChallenge').val('')
            $gameCaptcha.find('input#gameCaptchaResponse').val('')
            loadBoard($gameCaptcha, options)


gameCaptchaError = (error) ->
    $("div#gameCaptchaError").html(error)
