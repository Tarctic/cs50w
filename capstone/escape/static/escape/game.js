const { useState, useEffect } = React;

const Start = ({id, Game, save }) => {

    // State to switch between main menu, Instructions and About windows
    const [what,setWhat] = useState('menu')

    // Checking if user is logged in and if yes, whether the logged in user has played before in order to display relevant buttons.
    if (id!=0) {
        var cont = true
        if (save==0) {
            var cont = false
        }
        var login = false;
    }
    else {
        var cont = false;
        var login = true;
    }

    return(
        <div>
            {/* Main menu */}
            {what=='menu' && <div className="center d-flex flex-column">
                <button className="bt p-2" onClick={() =>{Game(0)}}>NEW GAME</button>
                {cont && <button className="bt p-2" onClick={() =>{Game(1)}}>CONTINUE</button>}
                {login && <button className="bt p-2" onClick={() =>  window.location.href='/login'}>Login</button>}
                <button className="bt p-2" onClick={() => setWhat('how')}>Instructions</button>
                <button className="bt p-2" onClick={() => setWhat('about')}>About</button>
            </div>}

            {/* Instructions */}
            {what=='how' && <div className="window">
                <h1><u>How To Play</u></h1>
                <br></br>
                <ol className="windowtext">
                    <li>CLICK ON BUBBLE SPEECHES TO PROCEED.</li>
                    <li>SOME OBJECTS ARE STORED IN THE INVENTORY WHEN CLICKED WHILE OTHERS RESPOND. SOME OBJECTS DO NOT RESPOND AT ALL.</li>
                    <li>OBJECTS IN THE INVENTORY ARE HIGHLIGHTED WHEN CLICKED. THIS MEANS THAT THEY ARE CURRENTLY IN USE.</li>
                    <li>ARROWS ARE USED TO MOVE BETWEEN ROOMS OR AREAS.</li>
                </ol>
                <h4>NOTE: PROGRESS IS ONLY SAVED IF YOU ARE LOGGED IN</h4>
                <button className="backbtn" onClick={() => setWhat('menu')}>BACK</button>
            </div>}

            {/* About */}
            {what=='about' && <div className="window">
                <h1>ABOUT</h1>
                <br></br>
                <p className="windowtext">THIS GAME WAS CREATED AS A PROTOTYPE TO TEST THE FEATURES TO IMPLEMENT IN THE GAME I ORIGINALLY HAD IN MIND. BUT I ENDED UP GETTING TOO INVESTED IN TRYING OUT NEW FEATURES AND RAN OUT OF TIME :)</p>
                <h4>Game created by Tarctic</h4>
                <button className="backbtn" onClick={() => setWhat('menu')}>BACK</button>
            </div>}
        </div>
    )
}

const Main = ({ save, saveGame, START }) => {

    // State to set background
    const [bg, setBg] = useState('bg1')
    // State to set a list of objects to be displayed
    const [obj, setObj] = useState(['inv',0,'door1','door2','clock','db','mc1','text1','dbclick'])
    // State to set items in the inventory
    const [items, setItem] = useState(['','','','','','','','','',])
    // State to set text of the speech bubbles
    const [text, setText] = useState()
    // State to set whether the character is speaking
    const [speaking, setSpeaking] = useState(true)
    // State to set if the object in inventory is highighted
    const [box,setBox] = useState({
        keyinv: false,
        paperinv: false
    })

    // function to continue the game where the user left off (setting the right state)
    const openSave = () => {
        console.log("save: " + save)
        if (save==1) {
        setBg('bg1')
        setObj(['inv', 0, 'door1', 'door2', 'clock', 'db', 'mc1'])
            setItem(['keyinv','','','','','','','','',])
        } 
        else if (save==2) {
            panel2()
        }
        else if (save==3) {
            panel2()
            setItem(['paperinv','','','','','','','','',])
        } 
        else if (save==4) {
            panel3()
            setItem(['paperinv','','','','','','','','',])
        } 
        else if (save==5) {
            panel4()
        }
    }

    // function to add and delete objects from the state list (to display or remove objects in game)
    const delAddObj = (d,a) => {
        console.log(d,a)
        var newObj = [...obj]
        if (d!=0) {
            newObj = obj.filter((o) => o!=d)
        }
        if (a!=0) {
            newObj.push(a)
        }
        setObj(newObj)
    }
    
    // function to add items to inventory
    const addToInv = (item) => {
        const newItem = [...items]
        var n = 0;
        for (var i=0;i<newItem.length;i++) {
            var p = newItem[i]
            if (p=='') {
                n = i;
                break
            }
        }
        newItem[n] = item
        setItem(newItem)
    }

    //function to delete from inventory
    const delFromInv = (item) => {
        const newItem = [...items]
        var finalItem = []
        for (var i=0;i<newItem.length;i++) {
            var p = newItem[i]
            if (p!=item) {
                finalItem.push(p)
            }
            else {
                finalItem.push('')
            }
        }
        setItem(finalItem)
    }
    
    // functions to set the right state for each panel (room/area in the game)
    const panel2 = () => {
        setBg('bg2')
        const newObj = ['inv','left1','mc2','paint','textp',0]
        setObj(newObj)
    }
    const panel3 = () => {
        setBg('bg3')
        const newObj = ['inv','left2','right','mc3','nerd','text4']
        setObj(newObj)
    }
    const panel4 = () => {
        saveGame(5)
        setBg('end')
        setObj([])
        setTimeout(() => {
            setBg('endcard')
            setObj(['goback'])
        }, 10000);
    }

    // functions of each item in the inventory
    const func = (item) => {
        var namelist = ['keyinv','paperinv']
        var funclist = [key,paper]
        for (var i=0;i<namelist.length;i++) {
            if (item == namelist[i]) {
                funclist[i]()
            }
        }
        if (box[item]) {
            setBox({...box, keyinv: false})
        } else {
            setBox({...box, keyinv: true})
        }
    }
    const key = () => {
        if (obj.includes('key')) {
            delAddObj('key',0)
        } else {
            delAddObj(0,'key')
        }
    }
    const paper = () => {
        delAddObj(0,'bigpaper');
        delFromInv('paperinv')
    }
    
    // code to submit answer entered by the user and check if it's right
    const [code, setCode] = useState('')
    const onSubmit = (e) => {
        e.preventDefault()

        onAdd({ code })
        setCode('')
    }
    const onAdd = ({ code }) => {
        if (code == 'PGBDYU') {
            delAddObj('input','goleft')
        } else {
            delAddObj('input','text6')
        }
    }

    // function that adds, changes and removes the text of character in a single div
    const say = (thing) => {
        setText(thing)
        delAddObj(0,'text')
        setSpeaking(true)
    }

    // Making sure openSave() is run only once (to prevent an infinite loop)
    const [open, setOpen] = useState(true)
    if (open){ 
        openSave()
        setOpen(false)
    }

    return (
        <div className="outer">

            {/* background image (panel) */}
            <div className={`bg ${bg}`}>

            {/* inventory */}
            {obj.includes('inv') &&
            <div className="inv d-flex flex-row">
            {items.map((item) => (
                <div className={`p-2 inv-box ${box[item] ? 'h':'' }`}>
                    <div className={item} onClick={() => func(item)} ></div>
                </div>
            ))}
            </div>
            }

            {/* objects */}
            {obj.includes('door1') && <div className="door1" onClick={() => {if (!speaking) {say("It won't budge.")}}}></div>}
            {obj.includes('door2') && <div className="door2" onClick={() => {if (obj.includes('key')) {panel2();delFromInv('keyinv');saveGame(2)} else {if (!speaking) {say("It's locked... Who would've guessed?")}}}}></div>}
            {obj.includes('clock') && <div className="clock" onClick={() => {if (!speaking) {say("That clock is fast.")}}}></div>}
            {obj.includes('db') && <div className="dustbin" onClick={() => { if (!speaking && obj.includes('dbclick')) {addToInv('keyinv');delAddObj('dbclick','text');saveGame(1); setText("Of course! The best place to hide a key")}}}></div>}
            {obj.includes('mc1') && <div className="mc mc1"></div>}
            {obj.includes('text1') && <div className="text text1" onClick={() => {delAddObj('text1','text2');}}>I've been trapped here for hours</div>}
            {obj.includes('text2') && <div className="text text1" onClick={() => {delAddObj('text2','text3')}}>Who thought detention would be this bad</div>}
            {obj.includes('text3') && <div className="text text1" onClick={() => {setSpeaking(false),delAddObj('text3',0)}}>I need to find a way out . . .</div>}
            {obj.includes('text') && <div className="text text1" onClick={() => {setSpeaking(false),delAddObj('text',0)}}>{text}</div>}
            
            {obj.includes('mc2') && <div className="mc mc2"></div>}
            {obj.includes('textp') && <div className="text textp" onClick={() => {delAddObj('textp',0)}}>Is this what they call modern art?</div>}
            {obj.includes('left1') && <div className="left left1" onClick={() => {if (obj.includes('bigpaper')) {addToInv('paperinv'); saveGame(4)}; panel3(); if (items.includes('paperinv')) {saveGame(4)};}}></div>}
            {obj.includes('paint') && <div className="paint" onClick={() => {if (!items.includes('paperinv') && !obj.includes('bigpaper')) {delAddObj('paint','behind')}}}></div>}
            {obj.includes('behind') && <div className="behind"></div>}
            {obj.includes('behind') && <div className="paper" onClick={() => {delAddObj('behind','paint');addToInv('paperinv');saveGame(3);}}></div>}
            {obj.includes('bigpaper') && <div className="bigpaper" onClick={() => {delAddObj('bigpaper',0),addToInv('paperinv')}}></div>}

            {obj.includes('left2') && <div className="left left2" onClick={() => {if (obj.includes('goleft')) {panel4()}}}></div>}
            {obj.includes('right') && <div className="right" onClick={() => {panel2()}}></div>}
            {obj.includes('mc3') && <div className="mc mc3"></div>}
            {obj.includes('nerd') && <div className="nerd"></div>}
            {obj.includes('text4') && <div className="text text4" onClick={() => delAddObj('text4','text5')}>You shall not pass!</div>}
            {obj.includes('text5') && <div className="text text4" onClick={() => delAddObj('text5','input')}>*whispers* Unless you know the secret code...</div>}
            {obj.includes('input') && <form className="form" onSubmit={onSubmit}>
                <input type="text" value={code} onChange={(e) => setCode(e.target.value)}/>
                <input type="submit" />
            </form>}
            {obj.includes('goleft') && <div className="text text4" onClick={() => panel4()}>hehe go right ahead...</div>}
            {obj.includes('text6') && <div className="text text4" onClick={() => panel2()}>WRONG CODE! GO BACK!</div>}
            {obj.includes('goback') && <button className="goback" onClick={() => START()}> Main Menu</button>}
            </div>
        </div>
    )
}


function App() {

    // State to set save number indicating progress (which part of the game the user has reached)
    const [save, setSave] = useState(0)
    // State to set when <Main /> should be displayed (To prevent displaying until fetch has been loaded)
    const [main, setMain] = useState(false)
    // State to set when <Start /> should be displayed
    const [start, setStart] = useState(false)

    // to get id via index.html file
    const id = document.querySelector('#id').innerHTML

    // function to save game progress by sending POST request with save number
    const saveGame = (num) => {
        
        console.log("saving save no."+num)
        if (id!=0) {
            fetch(`/save/${id}`, {
                headers: {
                    'X-CSRFToken': csrf_token
                },
                method: 'POST',
                body: JSON.stringify({
                    data: num
                })
            })
        }
    }

    // function to display <Main />. Also, to save progress as 0 if 'new game' is clicked
    const Game = (num) => {
        if (num==0 && id!=0) {
               saveGame(0)
               setSave(0)
        }
        setMain(true)
        console.log('Main: save no.'+save)
    }
    
    // function to fetch progress via a get request and then display <Start />
    const START = () => {
        setMain(false)
        if (id!=0) {
        fetch(`/save/${id}`)
        .then(response => response.json())
        .then(res => {
            var save = res.savenum
            setSave(save)
            console.log('Start: fetched save no.'+save)
            setStart(true)
        })}
        else {setStart(true)}
    }

    // Making sure START() is run only once
    const [once, setOnce] = useState(true)
    if (once) {
        setOnce(false)
        START()
    }

    return (
        <div>
            <div className="outer">
                {!main && start && <div className="startbg">
                    <Start id={id} Game={Game} START={START} save={save} />
                </div>}
            </div>

            {main && <div>
                <Main save={save} saveGame={saveGame} START={START} />
            </div>}
        </div>
    );
}

ReactDOM.render(<App />, document.querySelector("#app"));