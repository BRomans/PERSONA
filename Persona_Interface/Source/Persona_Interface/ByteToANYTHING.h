// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "ByteToANYTHING.generated.h"


UCLASS( ClassGroup=(Custom), meta=(BlueprintSpawnableComponent) )
class PERSONA_INTERFACE_API UByteToANYTHING : public UActorComponent
{
	GENERATED_BODY()

public:	
	// Sets default values for this component's properties
	UByteToANYTHING();

protected:
	// Called when the game starts
	virtual void BeginPlay() override;

public:	
	// Called every frame
	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

	UFUNCTION(BlueprintCallable, Category = "byteeeee")
		FString StringFromBinaryArray(const TArray<uint8>& BinaryArray);

};
