// SPDX-License-Identifier: GPL-3.0-or-later

pragma solidity ^0.8.17;

import "./IGradebook.sol";

contract Gradebook is IGradebook {
    // A mapping to keep track of the tas
    mapping (address => bool) public override tas;
    // A mapping of the max score for each assignment
    mapping (uint => uint) public override max_scores;
    // A mapping of the name of each assignment
    mapping (uint => string) public override assignment_names;
    // A mapping of the score for a given student id for each assignment;
    // scores[assignment_id][student_name] = score
    mapping (uint => mapping(string => uint) ) public override scores;
    // How many assignments are there?
    uint public override num_assignments;
    // What is the instructor's address?
    address public override instructor;
    // The constructor, which runs when it's first deployed to the blockchain;
    // Whoever deploys the blockchain is the instructor
    constructor() {
        instructor = msg.sender;
    }
    // Designates the address as a t;
    // Only the instructor can designate tas
    function designateTA(address ta) public override {
        require(msg.sender == instructor, "Only the instructor can designate tas");
        tas[ta] = true;
    }
    // Adds an assignment with name and max_score;
    // Only the instructor or tas can add assignments
    // Assignments can have the same name
    // Returns the assignment's id
    function addAssignment(string memory name, uint max_score) public override returns (uint){
        require(msg.sender == instructor || tas[msg.sender], "Only the instructor or tas can add assignments");
        assignment_names[num_assignments] = name;
        max_scores[num_assignments] = max_score;
        uint id = num_assignments;
        emit assignmentCreationEvent(id);
        num_assignments++;
        return id;
    }
    // Adds student's score for an assignment
    // Only the instructor or tas can add grades
    // The assignment must exist
    // The score must not exceed the assignment's max score
    function addGrade(string memory student, uint assignment, uint score) public override {
        require(msg.sender == instructor || tas[msg.sender], "Only the instructor or tas can add grades");
        require(assignment < num_assignments, "The assignment does not exist");
        require(score <= max_scores[assignment], "The score exceeds this assignment's max score");
        scores[assignment][student] = score;
        emit gradeEntryEvent(assignment);
    }
    // Gets the average of a students points on all assignments (i.e. 16.667% is 1666 points);
    function getAverage(string memory student) public view returns (uint){
        uint student_points = 0;
        uint net_points = 0;
        for(uint i = 0; i < num_assignments; i++){
            student_points += scores[i][student];
            net_points += max_scores[i];
        }
        return (student_points * 10000) / net_points;
    }
    // Makes the caller a TA
    function requestTAAccess() public override {
        tas[msg.sender] = true;
    }
    // Checks the interfaceId
    function supportsInterface(bytes4 interfaceId) external pure returns (bool) {
        return interfaceId == type(IGradebook).interfaceId || interfaceId == 0x01ffc9a7;
    }
}