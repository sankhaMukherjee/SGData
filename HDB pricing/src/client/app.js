var app = angular.module( 'plotInfo' , []);

app.controller('plotInfoData', function ($scope, $http) {

    // This can be used for testing some functions ...
    var trace1 = {
      x: [1, 2, 3, 4],
      y: [10, 15, 13, 17],
      mode: 'markers',
      type: 'scatter'
    };

    var trace2 = {
      x: [2, 3, 4, 5],
      y: [16, 5, 11, 9],
      mode: 'lines',
      type: 'scatter'
    };

    var trace3 = {
      x: [1, 2, 3, 4],
      y: [12, 9, 15, 12],
      mode: 'lines+markers',
      type: 'scatter'
    };


    $scope.data = [trace1, trace2, trace3];

    /////////////////////////////////////////////////
    // Let us first put in the data here ...
    // We shall have a system that finds the 
    // following things.
    // 1. What are the columns that we will be 
    // dealing with
    // 2. What are the values that we shall be 
    // using for filtering. These are not general
    // in this case, and we shall be hard coding 
    // the values in here
    /////////////////////////////////////////////////
    $scope.filterData = {
        'town':{},
        'flat_type':{},
        'flat_model':{}
    };

    ///////////////////////////////////////////////////////////////////////
    // This function is used for obtaining the unique values of all the 
    // functions that we may be interested in filtering ...
    ///////////////////////////////////////////////////////////////////////
    $scope.getUnique = function (value) {
        $http.get('http://localhost:8080/data/unique/'+value).then( function (result) {
            $scope.filterData[value] = {};
            result['data'].forEach( function (m) {  $scope.filterData[value][m] = true; } );
        }, function (){
            $scope.data = 'There was a problem reading the data ...';
        });
    };

    // Lets the get the unique values for all the variables 
    // we are looking for ... 
    ['town', 'flat_type', 'flat_model'].forEach( $scope.getUnique )

    ////////////////////////////////////////////////////////////
    // This is the section that will contain the information 
    // for determining how to plot data, and what data to 
    // plot. 
    ////////////////////////////////////////////////////////////

    $scope.columns     = [];
    $scope.xColumn     = null;
    $scope.yColumn     = null;
    $scope.groupBy     = null;
    $scope.groupByI    = null;
    $scope.aggFunction = 'median';

    $scope.plotData = {

    };

    /////////////////////////////////////////
    // Lets update the columns, so that we
    // can use this to plot a bunch of 
    // things later ...
    $http.get('http://localhost:8080/data/raw/columns').then( function (result) {
        $scope.columns = [];
        result['data'].forEach( function (m) { $scope.columns.push(m); } );
    }, function (){
        $scope.data = 'There was a problem reading the data ...';
    });

    // Function to generate the value of the post request
    //  for obtaining the data to be plotted ...
    ///////////////////////////////////////////////////////
    $scope.generatePostData = function () {
        postData = {
            x    : $scope.xColumn,
            y    : $scope.yColumn,
            gBy  : $scope.groupBy,
            gByI : $scope.groupByI,
            agg  : $scope.aggFunction,
            townFilter:      [],
            flatTypeFilter:  [],
            flatModelFilter: [],
        };

        for (var key in $scope.filterData['town']) {
            if ( $scope.filterData['town'][key] ) { postData.townFilter.push(key); };
        };

        for (var key in $scope.filterData['flat_type']) {
            if ( $scope.filterData['flat_type'][key] ) { postData.flatTypeFilter.push(key); };
        };

        for (var key in $scope.filterData['flat_model']) {
            if ( $scope.filterData['flat_model'][key] ) { postData.flatModelFilter.push(key); };
        };

        $http.post('http://localhost:8080/data/raw', postData).then( function (value) {
            $scope.data = value["data"];
        }, function () {} );

        return postData;
    };
    
});

app.directive('getFilterItems', function () {
    return {
        scope    : {
            filterData: '=data',
            v:'=v'
        },
        restrict : 'E', 
        templateUrl : 'getFilter.html'
    };
});


app.directive( 'scatterPlot', function () {

    ///////////////////////////////////////////
    // This is the link function ...
    function linkFunc(scope, element, attrs) {
        scope.$watch('data', function (plots) {
            var layout = {
                'width': attrs.width,
                'height': attrs.height,
                'pad':'0',
                'margin': { 't': 0, 'b':20, 'l':40, 'r':0 },
            };

            Plotly.newPlot(element[0], plots, layout);
        }, true);
    }

    return {
        link: linkFunc,
    };
});

