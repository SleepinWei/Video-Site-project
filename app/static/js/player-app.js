var art = new Artplayer({
    container: '.artplayer-app',
    url: 'templates/test.mp4',
    plugins: [
        artplayerPluginDanmuku({
            danmuku: 'static/assets/comment-science.xml',
            speed: 5,
            maxlength: 50,
            margin: [10, 100],
            opacity: 1,
            fontSize: 25,
            synchronousPlayback: false,
        }),
    ],
    controls: [
        {
            position: 'right',
            html: 'Hide',
            click: function () {
                art.plugins.artplayerPluginDanmuku.hide();
            },
        },
        {
            position: 'right',
            html: 'Show',
            click: function () {
                art.plugins.artplayerPluginDanmuku.show();
            },
        },
        {
            position: 'right',
            html: 'Send',
            click: function () {
                var text = prompt('Please enter', 'Danmu text');
                if (!text || !text.trim()) return;
                var color = '#' + Math.floor(Math.random() * 0xffffff).toString(16);
                art.plugins.artplayerPluginDanmuku.emit({
                    text: text,
                    color: color,
                    border: true,
                });
            },
        },
    ],
});

// Send a new danmu
// art.plugins.artplayerPluginDanmuku.emit({
//     text: '666', // Danmu text
//     time: 5, // Video time
//     color: '#fff', // Danmu color
//     size: 25, // Danmu size
//     border: false, // Danmu border
//     mode: 0, // Danmu mode: 0-scroll or 1-static
// });

// Hide the danmu
// art.plugins.artplayerPluginDanmuku.hide();

// Show the danmu
// art.plugins.artplayerPluginDanmuku.show();

// Returns whether to hide the danmu
// art.plugins.artplayerPluginDanmuku.isHide;

// Config danmu dynamically
// art.plugins.artplayerPluginDanmuku.config({
//     // option
// });
