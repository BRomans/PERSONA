// Fill out your copyright notice in the Description page of Project Settings.


#include "ByteToANYTHING.h"

// Sets default values for this component's properties
UByteToANYTHING::UByteToANYTHING()
{
	// Set this component to be initialized when the game starts, and to be ticked every frame.  You can turn these features
	// off to improve performance if you don't need them.
	PrimaryComponentTick.bCanEverTick = true;

	// ...
}


// Called when the game starts
void UByteToANYTHING::BeginPlay()
{
	Super::BeginPlay();

	// ...
	
}


// Called every frame
void UByteToANYTHING::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

	// ...
}

FString UByteToANYTHING::StringFromBinaryArray(const TArray<uint8>& BinaryArray)
{
	
	FString Result = FString(UTF8_TO_TCHAR(BinaryArray.GetData()));

	return Result;
}

