#include "common.h"

using namespace std;

#define NAME "cpp"
#define COLOR "00ff00"

//############GLOBALS#################################################################################
World world;
long double myRange;
Coordinates defaultTarget{0,0};
int turn = 0;

//################HELPER##############################################################################
long double randRange(int a,int b){
    return (long double) (rand()%(b-a) + a);
}
Coordinates findCloseEntity(Player &myself){
    Coordinates close{1e18,1e18};
    long double minD = 1e18;
	for (Entity e : world.entities) {
		if (distance(e.position, myself.position) < minD) {
			close = e.position;
			minD = distance(e.position, myself.position);
		}
	}
    return close;
}

int findClosePlayerId(Player myself) {
    cerr << "CALLED CLOSE PLAYER" <<endl;
    int id = 1;
    long double minD = 1e18;
    for (Player e : world.players){
        cerr << abs(e.position - myself.position)<<endl;
        cerr << e.position << endl;
        if (abs(e.position - myself.position) < minD && abs(e.position - myself.position) != 0) {
            id = e.id;
            minD = distance(e.position, myself.position);
        }
    }
    return id;
}

Coordinates findClosePlayer(Player myself) {
    cerr << "CALLED CLOSE PLAYER" <<endl;
    Coordinates close{ 0,0 };
    long double minD = 1e18;
    for (Player e : world.players){
        cerr << abs(e.position - myself.position)<<endl;
        cerr << e.position << endl;
        if (abs(e.position - myself.position) < minD && abs(e.position - myself.position) != 0) {
            close = e.position;
            minD = distance(e.position, myself.position);
        }
    }
    return close;
}

//################LEVEP UP############################################################################
//                                             X                   X
vector<int> hardCodedLevelup{4,2,5,5,4,2,9,1,9,4,5,1,2,1,3,2,5,5,3,4,4,4,3,1,9,3,1,2,1,1};
Stat nextLevelup(){
    int curLevelup = world.level - world.levels_left;
    if(world.levels_left == 0) return Stat::None;
    if(curLevelup > hardCodedLevelup.size()) return Stat{rand()%10};
    else return Stat{hardCodedLevelup[curLevelup]};
}
vector<int> hardCodedUpgrade{5,7};
Tank nextUpgrade(){
    if(world.players[0].tankType == Tank::Basic) return (Tank) 5;
    return (Tank) 7;
}

//################SHOOTING############################################################################
long double smartShootAt(Player myself,Coordinates target){ //if out of range, shoot behind
    Coordinates vec = target - myself.position;
    Coordinates tmp{1,0};
    if(abs(vec) > myRange) tmp = Coordinates{-1,0};
    return arg(vec*tmp);
}

long double shoot(Player myself) {
    if (findClosePlayer(myself) != Coordinates{ 0, 0 }) {
        return smartShootAt(myself, findClosePlayer(myself));
    }
    return smartShootAt(myself, findCloseEntity(myself));
}

long double randomShoot(Player myself){
    long double offset = 2*3.14/360*(rand()%10 - 5);
    return shoot(myself)+offset;
}

//################MOVEMENT############################################################################ 
Coordinates moveInFront(Coordinates to, long double distance, Coordinates me) {
	Coordinates way = to - me;
	Coordinates real_to = (way / abs(way)) * (abs(way) - distance);
	cerr << "Going to: " << real_to << endl;
	return real_to;
}

void checkFinalDestination(Coordinates &dest){
    Coordinates kam = dest/abs(dest)*world.stat_values[(int) Stat::Speed];
    kam += world.players[0].position;
    if(kam.x < world.min_x || kam.x > world.max_x || kam.y < world.min_y || kam.y > world.max_y){
        dest = defaultTarget;
        cerr << "IDEM SA HYBAT DO PREC"<<endl;
    }
}

Coordinates move(Player myself, long double range) {
    Coordinates close = findCloseEntity(myself);
	return moveInFront(close,60 + 2*myself.radius, myself.position);
	/*
	int closestK = 5;
	vector<Entity> balls = world.entities;
	sort(balls.begin(), balls.end(), [](const Entity& a, const Entity& b)
		{
			return distance(a.position, myself.position) > distance(b.position, myself.position);
		});
	vector<int> best(closestK);
	for (int i = 0; i < closestK; i++) {
		for (auto& j : balls) {
			if (distance(balls[i].position, j.position) < range) {
				best[i]++;
			}
		}
	}
	int targetI = max_element(best.begin(), best.end()) - best.begin();
	Entity target = balls[targetI];
	*/
}

bool willHit(Player myself, Bullet bullet){
    Coordinates vec = myself.position - bullet.position;
    Coordinates normal = (bullet.position - myself.position)*Coordinates{0,1};
    if(bullet.ttl*abs(bullet.velocity) < abs(vec) - myself.radius*2) return 0;
    long double hitAngle = atan((myself.radius + bullet.radius)/abs(vec));
    long double myAngle = arg(bullet.velocity) - arg(vec);
    if(abs(myAngle) <= abs(hitAngle)){ //it will hit
        return 1;
    }
    return 0;
}

bool enemyBullets(Player myself){
    for(Bullet b : world.bullets){
        if(b.shooter_id != myself.id) return 1;
    }
    return 0;
}

//dodge incoming bullets
Coordinates dodgeNormalVector(Player &myself, Bullet &bullet){
    if(myself.id == bullet.shooter_id) return Coordinates{0,0};
    Coordinates vec = myself.position - bullet.position;
    Coordinates normal = (bullet.position - myself.position)*Coordinates{0,1}; if(bullet.ttl*abs(bullet.velocity) < abs(vec) - myself.radius*2) return Coordinates{0,0}; //nestihne ma to trafit
    long double hitAngle = atan((myself.radius + bullet.radius)/abs(vec));
    long double myAngle = arg(bullet.velocity) - arg(vec);
    if(abs(myAngle) <= abs(hitAngle)){ //it will hit
        cerr<<"SANCA NA HIT"<<endl;
        if(myAngle >= 0){ //nadomnou

        }else{ //podomnou

        }
        return normal/abs(normal);
    }else{
        return Coordinates{0,0};
    }
}

//nepriamo umerne casu kym zasiahne, nepriamo umerne mojej rychlosti
Coordinates dodge(Player &myself){
    Bullet bullet;
    long double dist = 0;
    for(Bullet b : world.bullets){
        if(b.shooter_id != myself.id && willHit(myself,b) && dist > abs(b.position - myself.position)){
            bullet = b;
            dist = abs(b.position - myself.position);
        }
    }
    cerr << "DODGE OD "<<bullet.position<<endl;
    Coordinates vec = myself.position - bullet.position;
    //long double timeToDodge = 2*(myself.radius)/world.stat_values[Stat::Speed];
    return vec*dodgeNormalVector(myself,bullet);
}
//###########MAIN##################################################################################### 

// sem pis svoj kod
Command do_turn() {
    turn++;
    Player myself = world.players[0];
    for(auto i : world.players){
        if(i.id == world.my_id) myself = i;
    }
    myRange = world.stat_values[3] * world.stat_values[4]; //speed * ttl
    //kam ideme
    while(turn++ % 300 == 0 || defaultTarget.x < world.min_x || defaultTarget.x > world.max_x || defaultTarget.y < world.min_y || defaultTarget.y > world.max_y || abs(defaultTarget - myself.position) < 0.5*world.stat_values[(int) Stat::Range]){
        defaultTarget = Coordinates{randRange(world.min_x,world.max_x),randRange(world.min_y,world.max_y)};
    }
    cerr << "MyRange: " << myRange << endl;
    cerr<<"MOJA POZICIA "<<myself.position<<endl;
    Command command;
    bool fight = 0;
    if(world.level >= 24 || world.max_x - world.min_x < myRange*3 || world.max_y - world.min_y < myRange*3) fight = 1;
    if(fight) cerr << "SOM AGRESIVNY "<<world.players.size()<<endl;
    //if(world.level >= 26) fight = 1;
    Coordinates enemyPos = findClosePlayer(myself);
    command.shoot = ShootType::OneBullet;
    command.angle = shoot(myself);
    command.new_tank_id = nextUpgrade();
    command.stat = nextLevelup();
    if (myself.tankType != Tank::GuidedBullet && enemyPos == Coordinates{ 0, 0 }) { //nenasli sme hraca
        command.new_position = move(myself, myRange);
    }
    else if(myself.tankType == Tank::GuidedBullet) { //nasli sme hraca a ideme ho zabit
        long double safeDist = world.stat_values[(int)Stat::Range]*0.9;
        //long double safeDist = 0;
        Coordinates to = moveInFront(enemyPos, safeDist, myself.position);
        
        Coordinates side{0,0};
        if (abs(to) < world.stat_values[(int)Stat::Speed]) {
            side = ((enemyPos - myself.position)/ abs((enemyPos - myself.position))) * Coordinates{ 0, 1 }*Coordinates{ world.stat_values[(int)Stat::Speed], 0 };
        }
        
        if(enemyPos == Coordinates{0,0}){
            cerr <<"OUT OF RANGE"<<endl;
            Coordinates entity = findCloseEntity(myself);
            if(entity != Coordinates{1e18,1e18}){
                command.shoot = ShootType::Coords;
                command.follow_coordinates = entity;
            }
            command.new_position = defaultTarget - myself.position;
        }else if(abs(enemyPos - myself.position) < myRange){
            command.shoot = ShootType::Player;
            command.follow_player_id = findClosePlayerId(myself);
            command.new_position = to;
        }else{
            command.new_position = enemyPos - myself.position;
        }

        //add dodge
        if(enemyBullets(myself)){
            command.new_position += side;
        }
    }
    else if (fight) { //nie sme guided, ale ideme utocit
        long double safeDist = myRange*0.8;
        Coordinates to = moveInFront(enemyPos, safeDist, myself.position);
        command.angle = shoot(myself);
        command.new_position = to;
    }
    else { //nasli sme hraca a ideme prec
        Coordinates to{0, 0};
        if (abs(findCloseEntity(myself) - myself.position) < 70) { //konnstas dyyy
            to += moveInFront(findCloseEntity(myself), 70, myself.position);
        }
        to -= (enemyPos - myself.position);
        command.new_position = to;
    }
    cerr<<command<<endl;
    checkFinalDestination(command.new_position);
    cerr<<"KONIEC KOLA"<<endl;
    cerr<<command<<endl;
    return command;
}

int main() {
    // aby sme mali nahodu
    srand(time(nullptr));
    // robime tahy kym sme zivy
    do {
        cin >> world;
        cout << do_turn();
    } while (true);
    cout << "Bye\n";
}

