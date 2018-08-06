const INCREMENT = 5;

function increment(index) {
    // Update Pie Charts
    mypiechart_1.data.datasets[0].data[index] += INCREMENT;
    mypiechart_2.data.datasets[0].data[index] += INCREMENT;
    mypiechart_3.data.datasets[0].data[index] += INCREMENT;
    mypiechart_1.update();
    mypiechart_2.update();
    mypiechart_3.update();
    // Update Line Charts
    mylinechart_1.data.datasets[0].data[6] += INCREMENT;
    mylinechart_2.data.datasets[0].data[3] += INCREMENT;
    mylinechart_3.data.datasets[0].data[11] += INCREMENT;
    mylinechart_1.update();
    mylinechart_2.update();
    mylinechart_3.update();
}

socket = io.connect('http://feedme.georgeyu.cn:8000');

socket.on('new', raw => {
    index = parseInt(raw[1]) - 1;
    increment(index);
});
