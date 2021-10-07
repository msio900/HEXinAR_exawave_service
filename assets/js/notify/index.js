'use strict';
var notify = $.notify('<i class="fa fa-bell-o"></i><strong>페이지 불러오는중</strong> 이 페이지를 닫지 마세요...', {
    type: 'theme',
    allow_dismiss: true,
    delay: 2000,
    showProgressbar: true,
    timer: 300
});

setTimeout(function() {
    notify.update('message', '<i class="fa fa-bell-o"></i><strong>내부정보</strong> 불러오는 중');
}, 1000);
