.PHONY: clean_data

CXX = c++
CXXFLAGS = -Wall -O2 -g

SRC_DIR = src
OBJ_DIR = obj
BIN_DIR = bin
LIB_DIR = include

C++_TARGET = $(BDIR)/c++_main

# Creating directories if necessary
$(shell mkdir -p $(OBJ_DIR) $(BIN_DIR))

# Trouver tous les fichiers sources
SRCS = $(wildcard $(SRC_DIR)/*.cpp)

# Générer les fichiers objets correspondants
OBJS = $(patsubst $(SRC_DIR)/%.cpp, $(OBJ_DIR)/%.o, $(SRCS))

# Nom de l'exécutable final
TARGET = $(BIN_DIR)/mon_programme

# Règle de compilation finale
$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) $^ -o $@

# Règle pour compiler chaque .cpp en .o
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Nettoyage des fichiers objets et de l'exécutable
clean:
	rm -rf $(OBJ_DIR)/* $(TARGET)

# Compilation complète et exécution
run: $(TARGET)
	./$(TARGET) 1
	python3 display.py 1

bindings:
	make -C swig/

clean_data:
	rm -f data/*