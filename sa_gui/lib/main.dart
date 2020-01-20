import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Sentiment Analysis Runner',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(title: 'Sentiment Analysis Home Page'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);
  final String title;
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0;

  void _showHelp() {
    print('showHelp clicked');
    setState(() {
      _counter++;
    });
  }

  void _submit() async {
    print('submit clicked');
    // need to swap out hostname
    var host = '10.0.2.2';
    var response = await http.get('http://'+host+':5000/nlp/sa/all?data='+inputController.text);
    print('Response status: ${response.statusCode}');
    print('Response body: ${response.body}');
  }

  final inputController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: ListView(
        children: <Widget>[

        Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
//          crossAxisAlignment: CrossAxisAlignment.center,
            children: <Widget>[
              Padding(padding: EdgeInsets.only(top: 20.0)),
              Text('Sentiment Multi Analyzer',
                style: new TextStyle(color: Colors.blue, fontSize: 25.0),),
              Padding(padding: EdgeInsets.only(top: 50.0)),
              TextFormField(
                controller: inputController,
                maxLines: 3,
                decoration: new InputDecoration(
                  labelText: "New Text to Analyze",
                  fillColor: Colors.white,
                  border: new OutlineInputBorder(
                    borderRadius: new BorderRadius.circular(25.0),
                    borderSide: new BorderSide(
                    ),
                  ),
                  //fillColor: Colors.green
                )
              ),
              FlatButton(
                child: Text('Go'),
                onPressed: _submit,
              ),
              Padding(padding: EdgeInsets.only(top: 22.0)),
              Text('Results',
                style: new TextStyle(color: Colors.blue, fontSize: 15.0),),
              DataTable(
                columns: [
                  DataColumn(label: Text('Model')),
                  DataColumn(label: Text('Raw Score'), numeric: true),
                  DataColumn(label: Text('Sentiment')),
                ],
                rows: [
                  DataRow(
                    cells: [
                      DataCell(
                        Text('nltk'),
                      ),
                      DataCell(
                        Text('0.88'),
                      ),
                      DataCell(
                        Text('Positive'),
                      ),
                    ],
                  ),
                  DataRow(
                      cells: [
                        DataCell(
                          Text('Vader'),
                        ),
                        DataCell(
                          Text('0.81'),
                        ),
                        DataCell(
                          Text('Positive'),
                        ),
                      ]
                  ),
                  DataRow(
                      cells: [
                        DataCell(
                          Text('BERT'),
                        ),
                        DataCell(
                          Text('0.92'),
                        ),
                        DataCell(
                          Text('Very Positive'),
                        ),
                      ]
                  )
                ]
              )

            ],
          ),
        ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _showHelp,
        tooltip: 'Help',
        child: Icon(Icons.help),
      ), // This trailing comma makes auto-formatting nicer for build methods.
    );
  }
}
