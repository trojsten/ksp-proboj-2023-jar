#include "common.h"

using namespace std;

#define NAME "cpp"
#define COLOR "00ff00"

int DX[] = {0, 1, 0, -1};
int DY[] = {-1, 0, 1, 0};

World world;

// sem pis svoj kod
Command do_turn() {
    Player &myself = world.players[world.my_id];
    Command command;
    //cerr << world.players;
    //cerr << myself;

    return command;
}

int main() {
    // aby sme mali nahodu
    srand(time(nullptr));
    // povieme serveru ako sa chceme volat a farbu
    greet_server(NAME, COLOR);
    // robime tahy kym sme zivy
    do {
        cin >> world;
        cout << do_turn() << '.' << std::endl;
    } while (world.players[world.my_id].alive);
    cout << "Bye\n";
}

