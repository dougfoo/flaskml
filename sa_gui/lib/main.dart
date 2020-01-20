import 'dart:ui';

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
    print(inputController.text);
    
    dataList.add({"Model": "Foo", "Raw Score": ".67", "Sentiment": "Positive", "More Info": "Link to Google"});

    setState(() { });  // drive update to GUI
  }

  final inputController = TextEditingController();

  final List<Map<String, String>> dataList = [
    {"Model": "BERT", "Raw Score": "1", "Sentiment": "Very Positive", "More Info": "Link to BERT"},
    {"Model": "Azure", "Raw Score": ".8", "Sentiment": "Postitive", "More Info": "Link to MSFT"},
    {"Model": "Google", "Raw Score": ".7", "Sentiment": "Positive", "More Info": "Link to Google"},
  ];

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
              Padding(padding: EdgeInsets.only(top: 25.0)),
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: TextFormField(
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
              ),
               FlatButton (
                child: Text('Go'),
                color: Colors.blue,
                textColor: Colors.white,
                onPressed: _submit,
              ),
              Divider(),
              Padding(padding: EdgeInsets.only(top: 22.0)),
              Text('Results',
                style: new TextStyle(color: Colors.blue, fontSize: 15.0),),
              Container(
                margin: new EdgeInsets.all(10.0),
                color: Colors.green[50],
                child: Column (
                  children: <Widget>[
                    ConstrainedBox(
                      constraints: BoxConstraints(minWidth: 600),
                      child: DataTable(
                          columns: [
                            DataColumn(label: Text('Model', style: new TextStyle(fontWeight: FontWeight.bold, color:Colors.blue, fontSize: 15.0), )),
                            DataColumn(label: Text('Raw Score', style: new TextStyle(fontWeight: FontWeight.bold, color:Colors.blue, fontSize: 15.0),), numeric: true),
                            DataColumn(label: Text('Sentiment', style: new TextStyle(fontWeight: FontWeight.bold, color:Colors.blue, fontSize: 15.0),)),
                            DataColumn(label: Text('More Info', style: new TextStyle(fontWeight: FontWeight.bold, color:Colors.blue, fontSize: 15.0),)),
                          ],
                          rows:
                            dataList // Loops through dataColumnText, each iteration assigning the value to element
                              .map(((element) => DataRow(
                                cells: <DataCell>[
                                  DataCell(Text(element["Model"])), //Extracting from Map element the value
                                  DataCell(Text(element["Raw Score"])),
                                  DataCell(Text(element["Sentiment"])),
                                  DataCell(Text(element["More Info"])),
                                ],
                              )),
                            ).toList(),
                      ),
                    ),
                    Text('Evaluated: ',  style: new TextStyle(color: Colors.orange, fontWeight: FontWeight.bold, fontSize: 15.0),),
                    Text(inputController.text, style: new TextStyle(color: Colors.orange, fontStyle: FontStyle.italic, fontSize: 15.0),),
                  ],
                ),
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
