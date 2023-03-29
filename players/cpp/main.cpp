#include "common.h"

using namespace std;

#define NAME "cpp"
#define COLOR "00ff00"

World world;

// sem pis svoj kod
Command do_turn() {
    Player &myself = world.players[world.my_id];
    Command command;

    command.new_position = {20,20};
    command.shoot = ShootType::OneBullet;
    command.angle = 0.2;
    cerr << command << '\n';
    //cerr << myself;

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
    //cout << "Bye\n";
}

